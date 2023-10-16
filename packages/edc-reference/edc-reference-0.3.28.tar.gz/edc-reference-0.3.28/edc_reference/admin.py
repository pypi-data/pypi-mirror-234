from __future__ import annotations

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from edc_appointment.utils import get_appointment_model_cls
from edc_dashboard import url_names
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_sites.admin import SiteModelAdminMixin

from .admin_site import edc_reference_admin
from .models import Reference


@admin.register(Reference, site=edc_reference_admin)
class ReferenceAdmin(SiteModelAdminMixin, ModelAdminSubjectDashboardMixin, admin.ModelAdmin):
    date_hierarchy = "report_datetime"

    list_display = (
        "identifier",
        "dashboard",
        "model",
        "report_datetime",
        "visit",
        "timepoint",
        "field_name",
        "value",
    )
    list_filter = ("model", "timepoint", "field_name")
    search_fields = (
        "identifier",
        "value_str",
        "value_int",
        "value_date",
        "value_datetime",
        "value_uuid",
    )

    def visit(self, obj=None):
        return f"{obj.visit_code}.{obj.visit_code_sequence}"

    def get_subject_dashboard_url(self, obj=None) -> str | None:
        opts = {}
        if obj:
            try:
                appointment = get_appointment_model_cls().objects.get(
                    schedule_name=obj.schedule_name,
                    site=obj.site,
                    subject_identifier=obj.subject_identifier,
                    visit_code=obj.visit_code,
                    visit_code_sequence=obj.visit_code_sequence,
                    visit_schedule_name=obj.visit_schedule_name,
                )
            except ObjectDoesNotExist:
                pass
            else:
                opts = dict(appointment=str(appointment.id))
        return reverse(
            url_names.get(self.subject_dashboard_url_name),
            kwargs=dict(subject_identifier=obj.subject_identifier, **opts),
        )

    def dashboard(self, obj=None, label=None) -> str:
        url = self.get_subject_dashboard_url(obj=obj)
        context = dict(title="Go to subject's dashboard", url=url, label=label)
        return render_to_string("dashboard_button.html", context=context)
