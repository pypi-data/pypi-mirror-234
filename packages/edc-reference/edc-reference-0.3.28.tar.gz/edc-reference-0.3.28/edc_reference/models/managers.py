from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

if TYPE_CHECKING:
    from edc_reference.models import Reference


class ReferenceManager(models.Manager):
    def get_by_natural_key(
        self,
        identifier,
        visit_schedule_name,
        schedule_name,
        visit_code,
        timepoint,
        report_datetime,
        model,
        field_name,
    ):
        return self.get(
            identifier=identifier,
            visit_schedule_name=visit_schedule_name,
            schedule_name=schedule_name,
            visit_code=visit_code,
            timepoint=timepoint,
            report_datetime=report_datetime,
            model=model,
            field_name=field_name,
        )

    def filter_crf_for_visit(self, name=None, visit=None) -> Iterable[Reference]:
        """Returns a queryset of reference model instances
        for this model on this visit.
        """
        opts = dict(
            identifier=visit.subject_identifier,
            model=name,
            report_datetime=visit.report_datetime,
            visit_schedule_name=visit.visit_schedule_name,
            schedule_name=visit.schedule_name,
            visit_code=visit.visit_code,
            timepoint=visit.timepoint,
        )

        return self.filter(**opts)

    def get_crf_for_visit(
        self, name=None, related_visit=None, field_name=None
    ) -> Reference | None:
        """Returns an instance of reference model
        for this model on this visit for this field.

        visit is a visit model instance.
        """
        try:
            model_obj = self.get(
                identifier=related_visit.subject_identifier,
                model=name,
                report_datetime=related_visit.report_datetime,
                visit_schedule_name=related_visit.visit_schedule_name,
                schedule_name=related_visit.schedule_name,
                visit_code=related_visit.visit_code,
                timepoint=related_visit.timepoint,
                field_name=field_name,
            )
        except ObjectDoesNotExist:
            model_obj = None
        return model_obj

    def get_requisition_for_visit(self, name: str = None, related_visit=None) -> Reference:
        """Returns an instance of reference model
        for this requisition on this visit for this panel.

        visit is a related_visit model instance.
        """
        opts = dict(
            identifier=related_visit.subject_identifier,
            model=name,
            report_datetime=related_visit.report_datetime,
            visit_schedule_name=related_visit.visit_schedule_name,
            schedule_name=related_visit.schedule_name,
            visit_code=related_visit.visit_code,
            timepoint=related_visit.timepoint,
            field_name="panel",
        )
        try:
            model_obj = self.get(**opts)
        except ObjectDoesNotExist:
            model_obj = None
        return model_obj
