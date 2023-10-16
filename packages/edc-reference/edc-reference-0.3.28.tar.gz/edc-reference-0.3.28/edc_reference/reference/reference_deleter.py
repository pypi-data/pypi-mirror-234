from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from django.apps import apps as django_apps
from django.db import transaction

from ..site_reference import site_reference_configs

if TYPE_CHECKING:
    from edc_visit_tracking.model_mixins import VisitModelMixin

    from ..models import Reference


class ReferenceDeleterError(Exception):
    pass


class ReferenceDeleter:

    """A class to delete all instances from edc_reference.Reference
    model linked to this Crf or Requisition model instance.

    See signals and edc_reference.Reference.
    """

    def __init__(self, model_obj=None):
        reference_model = site_reference_configs.get_reference_model(
            name=model_obj.reference_name
        )
        self.model_obj = model_obj
        self.reference_model_cls: Reference = django_apps.get_model(reference_model)
        self.delete_reference_obj()

    def delete_reference_obj(self) -> None:
        with transaction.atomic():
            self.reference_model_cls.objects.filter(**self.options).delete()

    @property
    def options(self) -> dict[str, int | str | datetime]:
        """Returns query lookup options.

        Note: `Reference` model instances for requisitions use the
        `label_lower.panel_name` format for field `reference_name`.
        """
        opts = dict(
            identifier=self.related_visit.subject_identifier,
            report_datetime=self.related_visit.report_datetime,
            timepoint=self.related_visit.timepoint,
            model=self.reference_name,
        )
        if [x for x in opts.values() if x is None]:
            raise ReferenceDeleterError(
                f"Invalid query options. Null values not allowed. Got {opts}."
            )
        return opts

    @property
    def related_visit(self) -> VisitModelMixin:
        try:
            related_visit = self.model_obj.related_visit
        except AttributeError as e:
            raise ReferenceDeleterError(str(e))
        return related_visit

    @property
    def reference_name(self) -> str:
        try:
            reference_name = self.model_obj.reference_name
        except AttributeError as e:
            raise ReferenceDeleterError(str(e))
        return reference_name
