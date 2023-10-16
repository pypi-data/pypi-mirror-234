from dateutil.relativedelta import relativedelta
from django.contrib.sites.models import Site
from edc_constants.constants import NEG, POS
from edc_utils import get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.models import SubjectVisit

from edc_reference.models import Reference
from edc_reference.refsets import Refset, RefsetError
from reference_app.models import CrfOne
from reference_app.register_reference_configs import register_reference_configs
from reference_app.visit_schedules import visit_schedule1

from .test_case import TestCase


class TestRefset(TestCase):
    def setUp(self):
        site_visit_schedules._registry = {}
        site_visit_schedules.register(visit_schedule1)
        register_reference_configs()
        self.prepare_subject_visit("reference_app.onschedule")
        values = [
            (NEG, get_utcnow() - relativedelta(years=3)),
            (POS, get_utcnow() - relativedelta(years=2)),
            (POS, get_utcnow() - relativedelta(years=1)),
        ]
        for index, subject_visit in enumerate(
            SubjectVisit.objects.filter(subject_identifier=self.subject_identifier).order_by(
                "report_datetime"
            )
        ):
            CrfOne.objects.create(
                subject_visit=subject_visit,
                field_int=index,
                field_str=values[index][0],
                field_datetime=values[index][1],
                field_date=values[index][1].date(),
                site=Site.objects.get_current(),
            )

    def test_raises_model_not_in_site(self):
        self.assertRaises(
            RefsetError,
            Refset,
            name="reference_app.blah",
            subject_identifier=self.subject_identifier,
            report_datetime=self.subject_visits[0].report_datetime,
            visit_schedule_name=self.subject_visits[0].visit_schedule_name,
            schedule_name=self.subject_visits[0].schedule_name,
            visit_code=self.subject_visits[0].visit_code,
            timepoint=self.subject_visits[0].timepoint,
            reference_model_cls=Reference,
        )

    def test_raises_unknown_reference_model(self):
        self.assertRaises(
            RefsetError,
            Refset,
            name="reference_app.crfone",
            subject_identifier=self.subject_identifier,
            report_datetime=self.subject_visits[0].report_datetime,
            visit_schedule_name=self.subject_visits[0].visit_schedule_name,
            schedule_name=self.subject_visits[0].schedule_name,
            visit_code=self.subject_visits[0].visit_code,
            timepoint=self.subject_visits[0].timepoint,
            reference_model_cls=None,
        )

    def test_raises_missing_report_datetime(self):
        self.assertRaises(
            RefsetError,
            Refset,
            name="reference_app.crfone",
            subject_identifier=self.subject_identifier,
            report_datetime=None,
            visit_schedule_name=self.subject_visits[0].visit_schedule_name,
            schedule_name=self.subject_visits[0].schedule_name,
            visit_code=self.subject_visits[0].visit_code,
            timepoint=self.subject_visits[0].timepoint,
            reference_model_cls=Reference,
        )

    def test_raises_missing_subject_identifier(self):
        self.assertRaises(
            RefsetError,
            Refset,
            name="reference_app.crfone",
            subject_identifier=None,
            report_datetime=self.subject_visits[0].report_datetime,
            visit_schedule_name=self.subject_visits[0].visit_schedule_name,
            schedule_name=self.subject_visits[0].schedule_name,
            visit_code=self.subject_visits[0].visit_code,
            timepoint=self.subject_visits[0].timepoint,
            reference_model_cls=Reference,
        )

    def test_no_reference_instance(self):
        Reference.objects.all().delete()
        refset = Refset(
            name="reference_app.crfone",
            subject_identifier=self.subject_identifier,
            report_datetime=self.subject_visits[0].report_datetime,
            visit_schedule_name=self.subject_visits[0].visit_schedule_name,
            schedule_name=self.subject_visits[0].schedule_name,
            visit_code=self.subject_visits[0].visit_code,
            timepoint=self.subject_visits[0].timepoint,
            reference_model_cls=Reference,
        )
        for value in refset._fields.values():
            self.assertIsNone(value)

    def test_missing_reference_instance_for_one_field(self):
        Reference.objects.filter(field_name="field_str").delete()
        refset = Refset(
            name="reference_app.crfone",
            subject_identifier=self.subject_identifier,
            report_datetime=self.subject_visits[0].report_datetime,
            visit_schedule_name=self.subject_visits[0].visit_schedule_name,
            schedule_name=self.subject_visits[0].schedule_name,
            visit_code=self.subject_visits[0].visit_code,
            timepoint=self.subject_visits[0].timepoint,
            reference_model_cls=Reference,
        )
        self.assertIsNone(refset._fields.get("field_str"))

    def test_multiple_reference_instance_for_one_field1(self):
        refset = Refset(
            name="reference_app.crfone",
            subject_identifier=self.subject_identifier,
            report_datetime=get_utcnow(),
            visit_schedule_name=self.subject_visits[0].visit_schedule_name,
            schedule_name=self.subject_visits[0].schedule_name,
            visit_code=self.subject_visits[0].visit_code,
            timepoint=self.subject_visits[0].timepoint,
            reference_model_cls=Reference,
        )
        self.assertEqual(NEG, refset._fields.get("field_str"))

    def test_multiple_reference_instance_for_one_field2(self):
        refset = Refset(
            name="reference_app.crfone",
            subject_identifier=self.subject_identifier,
            report_datetime=get_utcnow(),
            visit_schedule_name=self.subject_visits[1].visit_schedule_name,
            schedule_name=self.subject_visits[1].schedule_name,
            visit_code=self.subject_visits[1].visit_code,
            timepoint=self.subject_visits[1].timepoint,
            reference_model_cls=Reference,
        )
        self.assertEqual(POS, refset._fields.get("field_str"))

        refset = Refset(
            name="reference_app.crfone",
            subject_identifier=self.subject_identifier,
            report_datetime=get_utcnow(),
            visit_schedule_name=self.subject_visits[2].visit_schedule_name,
            schedule_name=self.subject_visits[2].schedule_name,
            visit_code=self.subject_visits[2].visit_code,
            timepoint=self.subject_visits[2].timepoint,
            reference_model_cls=Reference,
        )
        self.assertEqual(POS, refset._fields.get("field_str"))

    def test_if_reference_exists_updates_report_datetime_in_fields(self):
        refset = Refset(
            name="reference_app.crfone",
            subject_identifier=self.subject_identifier,
            report_datetime=self.subject_visits[0].report_datetime,
            visit_schedule_name=self.subject_visits[0].visit_schedule_name,
            schedule_name=self.subject_visits[0].schedule_name,
            visit_code=self.subject_visits[0].visit_code,
            timepoint=self.subject_visits[0].timepoint,
            reference_model_cls=Reference,
        )
        for field, value in refset._fields.items():
            if field == "report_datetime":
                self.assertEqual(value, self.subject_visits[0].report_datetime)
            elif field == "timepoint":
                self.assertEqual(value, self.subject_visits[0].timepoint, msg=field)

    def test_if_reference_updates_fields(self):
        for index, subject_visit in enumerate(self.subject_visits):
            with self.subTest(index=index, subject_visit=subject_visit):
                refset = Refset(
                    name="reference_app.crfone",
                    subject_identifier=subject_visit.subject_identifier,
                    report_datetime=subject_visit.report_datetime,
                    visit_schedule_name=subject_visit.visit_schedule_name,
                    schedule_name=subject_visit.schedule_name,
                    visit_code=subject_visit.visit_code,
                    timepoint=subject_visit.timepoint,
                    reference_model_cls=Reference,
                )
                crf_one = CrfOne.objects.get(subject_visit=subject_visit)
                for field, value in refset._fields.items():
                    if field == "report_datetime":
                        self.assertEqual(value, subject_visit.report_datetime, msg=field)
                    elif field == "timepoint":
                        self.assertEqual(value, subject_visit.timepoint, msg=field)
                    else:
                        self.assertEqual(value, getattr(crf_one, field), msg=field)
