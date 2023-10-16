from dateutil.relativedelta import relativedelta
from django.contrib.sites.models import Site
from django.test import TestCase as BaseTestCase
from edc_appointment.constants import INCOMPLETE_APPT
from edc_appointment.models import Appointment
from edc_facility import import_holidays
from edc_utils import get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.constants import SCHEDULED
from edc_visit_tracking.models import SubjectVisit

from reference_app.models import SubjectConsent


class TestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        import_holidays()

    def prepare_subject_visit(
        self, onschedule_model: str, subject_identifier: str | None = None
    ):
        self.subject_identifier = subject_identifier or "12345"
        self.subject_visits = []

        subject_consent = SubjectConsent.objects.create(
            subject_identifier=self.subject_identifier,
            consent_datetime=get_utcnow() - relativedelta(days=14),
            identity=f"{subject_identifier}56789",
            confirm_identity=f"{subject_identifier}56789",
        )
        visit_schedule, schedule = site_visit_schedules.get_by_onschedule_model(
            onschedule_model
        )
        schedule.put_on_schedule(
            subject_identifier=subject_consent.subject_identifier,
            onschedule_datetime=subject_consent.consent_datetime,
        )

        for appointment in Appointment.objects.all().order_by("timepoint"):
            opts = dict(
                appointment=appointment,
                subject_identifier=self.subject_identifier,
                report_datetime=appointment.appt_datetime,
                reason=SCHEDULED,
                site=Site.objects.get_current(),
                visit_schedule_name=appointment.visit_schedule_name,
                schedule_name=appointment.schedule_name,
            )
            subject_visit = SubjectVisit.objects.create(**opts)
            self.subject_visits.append(subject_visit)
            appointment.appt_status = INCOMPLETE_APPT
            appointment.save()
