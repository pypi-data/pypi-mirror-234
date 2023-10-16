from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Type

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction

from ..site_reference import site_reference_configs

if TYPE_CHECKING:
    from ..models import Reference


class ReferenceGetterError(Exception):
    pass


class ReferenceObjectDoesNotExist(Exception):
    pass


class ReferenceGetter:
    """A class that gets the reference model instance for a given
    model or attributes of the model.

    See also ReferenceModelMixin.
    """

    def __init__(
        self,
        name: str | None = None,
        field_name: str | None = None,
        model_obj=None,
        related_visit=None,
        subject_identifier: str | None = None,
        report_datetime: datetime | None = None,
        visit_schedule_name: str | None = None,
        schedule_name: str | None = None,
        visit_code: str | None = None,
        visit_code_sequence: str | None = None,
        timepoint: Decimal | None = None,
        site=None,
        create: bool | None = None,
    ):
        self._object: Reference | None = None
        self.created: bool = False
        self.value = None
        self.has_value: bool = False

        self.create = True if create is None else create
        self.field_name = field_name
        if model_obj:
            if model_obj._meta.proxy:
                # always revert to the proxy_for_model
                model_obj = model_obj._meta.proxy_for_model.objects.get(id=model_obj.id)
            try:
                # given a crf model as model_obj
                self.name = model_obj.reference_name
                self.report_datetime = model_obj.related_visit.report_datetime
                self.schedule_name = model_obj.related_visit.schedule_name
                self.site = model_obj.related_visit.site
                self.subject_identifier = model_obj.related_visit.subject_identifier
                self.timepoint = model_obj.related_visit.timepoint
                self.visit_code = model_obj.related_visit.visit_code
                self.visit_code_sequence = model_obj.related_visit.visit_code_sequence
                self.visit_schedule_name = model_obj.related_visit.visit_schedule_name
            except AttributeError as e:
                if "related_visit" not in str(e):
                    raise
                # given a visit model as model_obj
                self.name = model_obj.reference_name
                self.report_datetime = model_obj.report_datetime
                self.schedule_name = model_obj.schedule_name
                self.site = model_obj.site
                self.subject_identifier = model_obj.subject_identifier
                self.timepoint = model_obj.timepoint
                self.visit_code = model_obj.visit_code
                self.visit_code_sequence = model_obj.visit_code_sequence
                self.visit_schedule_name = model_obj.visit_schedule_name
        elif related_visit:
            self.name = name
            self.report_datetime = related_visit.report_datetime
            self.schedule_name = related_visit.schedule_name
            self.site = related_visit.site
            self.subject_identifier = related_visit.subject_identifier
            self.timepoint = related_visit.timepoint
            self.visit_code = related_visit.visit_code
            self.visit_code_sequence = related_visit.visit_code_sequence
            self.visit_schedule_name = related_visit.visit_schedule_name
        else:
            # given only the attrs
            self.name = name
            self.report_datetime = report_datetime
            self.schedule_name = schedule_name
            self.site = site
            self.subject_identifier = subject_identifier
            self.timepoint = timepoint
            self.visit_code = visit_code
            self.visit_code_sequence = visit_code_sequence
            self.visit_schedule_name = visit_schedule_name

        reference_model: str = site_reference_configs.get_reference_model(name=self.name)
        if site_reference_configs.get_model(self.name)._meta.proxy:
            raise ReferenceGetterError(
                "May not be a proxy model. Provide the concrete model instead."
            )
        self.reference_model_cls: Type[Reference] = django_apps.get_model(reference_model)

        # note: updater needs to "update_value"
        # if 'object' does not exist, will be created
        self.value = getattr(self.reference_obj, "value")
        self.has_value = True
        setattr(self, self.field_name, self.value)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}({self.name}.{self.field_name}',"
            f"'{self.subject_identifier},{self.report_datetime}"
            f") value={self.value}, has_value={self.has_value}>"
        )

    @property
    def reference_obj(self) -> Reference:
        """Returns a reference model instance."""
        if not self._object:
            try:
                self._object = self.reference_model_cls.objects.get(**self.options)
            except ObjectDoesNotExist as e:
                if self.create:
                    try:
                        with transaction.atomic():
                            self._object = self.reference_model_cls.objects.create(
                                report_datetime=self.report_datetime, **self.options
                            )
                    except IntegrityError as e:
                        raise ReferenceGetterError(
                            f"Unable to create reference. Options=`{self.options}`. Got {e}"
                        )
                    self.created = True
                else:
                    raise ReferenceObjectDoesNotExist(
                        f"Unable to create reference. create=False! Options=`{self.options}`. "
                        f"Got {e}."
                    )
        return self._object

    @property
    def options(self) -> dict:
        opts = dict(
            identifier=self.subject_identifier,
            model=self.name,
            field_name=self.field_name,
            visit_schedule_name=self.visit_schedule_name,
            schedule_name=self.schedule_name,
            visit_code=self.visit_code,
            visit_code_sequence=self.visit_code_sequence,
            timepoint=self.timepoint,
            site=self.site,
        )
        if {k: v for k, v in opts.items() if v is None}:
            raise ReferenceGetterError(
                "Unable to get a reference instance. Null values for attrs "
                f"not allowed. {self}. Got {opts}."
            )
        if self.field_name not in [
            f.name for f in django_apps.get_model(self.label_lower)._meta.get_fields()
        ]:
            raise ReferenceGetterError(
                "Unable to get reference instance. Field does not exist on source model. "
                f"Got {self.label_lower}.{self.field_name}. See {self}."
            )

        return opts

    @property
    def label_lower(self) -> str:
        """Returns label_lower.

        Note: for `References` linked to requisitions, `Reference.model`
        is `app_label.model.panel_name`, for example,
        `my_app.subjectrequisition.glucose`.
        """
        return f"{self.name.split('.')[0]}.{self.name.split('.')[1]}"
