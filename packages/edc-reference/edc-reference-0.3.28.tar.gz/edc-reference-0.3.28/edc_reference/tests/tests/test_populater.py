from dateutil.relativedelta import relativedelta
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import NEG, POS
from edc_utils import get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from edc_reference.models import Reference
from edc_reference.populater import Populater
from reference_app.models import CrfOne, SubjectVisit
from reference_app.register_reference_configs import register_reference_configs
from reference_app.visit_schedules import visit_schedule1

from .test_case import TestCase


class TestPopulater(TestCase):
    def setUp(self):
        site_visit_schedules._registry = {}
        site_visit_schedules.register(visit_schedule1)
        register_reference_configs()
        self.prepare_subject_visit("reference_app.onschedule")
        dte = get_utcnow()
        self.crf_one_values = [
            (NEG, dte - relativedelta(years=3)),
            (POS, dte - relativedelta(years=2)),
            (POS, dte - relativedelta(years=1)),
        ]
        for index, subject_visit in enumerate(
            SubjectVisit.objects.filter(subject_identifier=self.subject_identifier).order_by(
                "report_datetime"
            )
        ):
            CrfOne.objects.create(
                subject_visit=subject_visit,
                field_int=index,
                field_str=self.crf_one_values[index][0],
                field_datetime=self.crf_one_values[index][1],
                field_date=self.crf_one_values[index][1].date(),
                site=Site.objects.get_current(),
            )

    def test_populates_for_visit(self):
        Reference.objects.all().delete()
        populater = Populater()
        populater.populate()
        for related_visit in SubjectVisit.objects.all():
            with self.subTest(report_datetime=related_visit.report_datetime):
                try:
                    Reference.objects.get(
                        identifier=self.subject_identifier,
                        model="edc_visit_tracking.subjectvisit",
                        report_datetime=related_visit.report_datetime,
                        field_name="report_datetime",
                        value_datetime=related_visit.report_datetime,
                    )
                except ObjectDoesNotExist as e:
                    self.fail(f"Object unexpectedly DoesNotExist. Got {e}")

    def test_populates_for_crfone_field_date(self):
        Reference.objects.all().delete()
        populater = Populater()
        populater.populate()
        for index, related_visit in enumerate(SubjectVisit.objects.all()):
            with self.subTest(report_datetime=related_visit.report_datetime):
                try:
                    Reference.objects.get(
                        identifier=self.subject_identifier,
                        model="reference_app.crfone",
                        report_datetime=related_visit.report_datetime,
                        field_name="field_date",
                        value_date=self.crf_one_values[index][1].date(),
                    )
                except ObjectDoesNotExist as e:
                    self.fail(f"Object unexpectedly DoesNotExist. Got {e}")

    def test_populates_for_crfone_field_datetime(self):
        Reference.objects.all().delete()
        populater = Populater()
        populater.populate()
        for index, related_visit in enumerate(SubjectVisit.objects.all()):
            with self.subTest(report_datetime=related_visit.report_datetime):
                try:
                    Reference.objects.get(
                        identifier=self.subject_identifier,
                        model="reference_app.crfone",
                        report_datetime=related_visit.report_datetime,
                        field_name="field_datetime",
                        value_datetime=self.crf_one_values[index][1],
                    )
                except ObjectDoesNotExist as e:
                    self.fail(f"Object unexpectedly DoesNotExist. Got {e}")

    def test_populates_for_crfone_field_str(self):
        Reference.objects.all().delete()
        populater = Populater()
        populater.populate()
        for index, related_visit in enumerate(SubjectVisit.objects.all()):
            with self.subTest(report_datetime=related_visit.report_datetime):
                try:
                    Reference.objects.get(
                        identifier=self.subject_identifier,
                        report_datetime=related_visit.report_datetime,
                        model="reference_app.crfone",
                        field_name="field_str",
                        value_str=self.crf_one_values[index][0],
                    )
                except ObjectDoesNotExist as e:
                    self.fail(f"Object unexpectedly DoesNotExist. Got {e}")

    def test_populates_for_crfone_field_int(self):
        Reference.objects.all().delete()
        populater = Populater()
        populater.populate()
        for index, related_visit in enumerate(SubjectVisit.objects.all()):
            with self.subTest(report_datetime=related_visit.report_datetime):
                try:
                    Reference.objects.get(
                        identifier=self.subject_identifier,
                        model="reference_app.crfone",
                        report_datetime=related_visit.report_datetime,
                        field_name="field_int",
                        value_int=index,
                    )
                except ObjectDoesNotExist as e:
                    self.fail(f"Object unexpectedly DoesNotExist. Got {e}")

    def test_populater_updates(self):
        populater = Populater()
        populater.populate()
        for index, related_visit in enumerate(SubjectVisit.objects.all()):
            with self.subTest(report_datetime=related_visit.report_datetime):
                try:
                    Reference.objects.get(
                        identifier=self.subject_identifier,
                        model="reference_app.crfone",
                        report_datetime=related_visit.report_datetime,
                        field_name="field_int",
                        value_int=index,
                    )
                except ObjectDoesNotExist as e:
                    self.fail(f"Object unexpectedly DoesNotExist. Got {e}")
