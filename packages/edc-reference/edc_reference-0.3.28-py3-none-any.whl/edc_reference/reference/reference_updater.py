from __future__ import annotations

from typing import TYPE_CHECKING

from ..site_reference import site_reference_configs
from .reference_getter import ReferenceGetter

if TYPE_CHECKING:
    from edc_model.models import BaseUuidModel
    from edc_visit_tracking.model_mixins import VisitTrackingCrfModelMixin

    from ..model_mixins import ReferenceModelMixin

    class AnyNonCrfModel(ReferenceModelMixin, BaseUuidModel):
        pass

    class AnyCrfModel(VisitTrackingCrfModelMixin, ReferenceModelMixin, BaseUuidModel):
        """Any CRF or Requisition model"""

        pass


class ReferenceFieldNotFound(Exception):
    pass


class ReferenceUpdaterModelError(Exception):
    pass


class ReferenceUpdater:
    """Updates or creates each reference model instance; one for
    each field in `edc_reference` for this model_obj.

    Will fail with a proxy model.
    """

    getter_cls = ReferenceGetter

    def __init__(self, model_obj: AnyNonCrfModel | AnyCrfModel | ReferenceModelMixin = None):
        self.model_obj = model_obj
        if self.model_obj._meta.proxy:
            self.model_obj = self.model_obj._meta.proxy_for_model.objects.get(id=model_obj.id)
            # raise ReferenceUpdaterModelError(
            #     "Not allowed. ReferenceUpdater does not accept proxy models. "
            #     f"Got `{self.model_obj.reference_name}`. "
            # )
        reference_fields = site_reference_configs.get_fields(
            name=self.model_obj.reference_name
        )
        # loop through fields and update or create each
        # reference model instance
        for field_name in reference_fields:
            try:
                field_obj = [
                    fld for fld in self.model_obj._meta.get_fields() if fld.name == field_name
                ][0]
            except IndexError:
                raise ReferenceFieldNotFound(
                    f"Reference field not found on model. Got '{field_name}'. "
                    f"See reference config for {self.model_obj.reference_name}. "
                    f"Model fields are "
                    f"{[fld.name for fld in self.model_obj._meta.get_fields()]}"
                )
            reference_getter = self.getter_cls(
                model_obj=self.model_obj, field_name=field_name, create=True
            )
            if field_obj.name == "report_datetime":
                try:
                    value = getattr(self.model_obj.related_visit, field_name)
                except AttributeError:
                    value = getattr(self.model_obj, field_name)
            else:
                value = getattr(self.model_obj, field_name)
            try:
                value = value.pk
            except AttributeError:
                internal_type = field_obj.get_internal_type()
                related_name = None
            else:
                internal_type = "UUIDField"
                related_name = getattr(self.model_obj, field_name)._meta.label_lower
            reference_getter.reference_obj.update_value(
                internal_type=internal_type,
                value=value,
                related_name=related_name,
            )
            reference_getter.reference_obj.save()

    def __repr__(self):
        return f"ReferenceUpdater({self.model_obj.__class__})"
