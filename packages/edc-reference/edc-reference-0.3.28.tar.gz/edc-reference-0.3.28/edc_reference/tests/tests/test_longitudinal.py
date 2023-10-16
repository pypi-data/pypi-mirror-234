from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.contrib.sites.models import Site
from edc_constants.constants import NEG, POS
from edc_utils import get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from edc_reference.models import Reference
from edc_reference.refsets import (
    InvalidOrdering,
    LongitudinalRefsets,
    NoRefsetObjectsExist,
)
from reference_app.models import CrfOne, SubjectVisit
from reference_app.register_reference_configs import register_reference_configs
from reference_app.visit_schedules import visit_schedule1

from .test_case import TestCase


class TestLongitudinal(TestCase):
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

    def test_longitudinal_refsets(self):
        refsets = LongitudinalRefsets(
            subject_identifier=self.subject_identifier,
            visit_model="edc_visit_tracking.subjectvisit",
            name="reference_app.crfone",
            reference_model_cls=Reference,
        )
        self.assertEqual(
            [refset.timepoint for refset in refsets],
            [Decimal("0.0"), Decimal("1.0"), Decimal("2.0")],
        )

    def test_longitudinal_refset_uses_subject_visit_report_datetime(self):
        longitudinal_refsets = LongitudinalRefsets(
            subject_identifier=self.subject_identifier,
            visit_model="edc_visit_tracking.subjectvisit",
            name="reference_app.crfone",
            reference_model_cls=Reference,
        )
        subject_visits = SubjectVisit.objects.filter(
            subject_identifier=self.subject_identifier
        ).order_by("report_datetime")
        report_datetimes = [obj.report_datetime for obj in subject_visits]
        self.assertEqual(
            [ref.report_datetime for ref in longitudinal_refsets], report_datetimes
        )
        self.assertEqual(
            [v.report_datetime for v in longitudinal_refsets.visit_references],
            report_datetimes,
        )

    def test_no_refsets(self):
        refsets = LongitudinalRefsets(
            subject_identifier=self.subject_identifier,
            visit_model="edc_visit_tracking.subjectvisit",
            name="reference_app.crfone",
            reference_model_cls=Reference,
        )
        refsets._refsets = []
        self.assertRaises(NoRefsetObjectsExist, refsets.fieldset, "field_name")

    def test_ordering(self):
        refsets = LongitudinalRefsets(
            subject_identifier=self.subject_identifier,
            visit_model="edc_visit_tracking.subjectvisit",
            name="reference_app.crfone",
            reference_model_cls=Reference,
        ).order_by("-report_datetime")
        self.assertEqual(
            [ref.timepoint for ref in refsets],
            [Decimal("2.0"), Decimal("1.0"), Decimal("0.0")],
        )
        refsets.order_by("-timepoint")
        self.assertEqual(
            [ref.timepoint for ref in refsets],
            [Decimal("2.0"), Decimal("1.0"), Decimal("0.0")],
        )
        refsets.order_by("report_datetime")
        self.assertEqual(
            [ref.timepoint for ref in refsets],
            [Decimal("0.0"), Decimal("1.0"), Decimal("2.0")],
        )
        refsets.order_by("timepoint")
        self.assertEqual(
            [ref.timepoint for ref in refsets],
            [Decimal("0.0"), Decimal("1.0"), Decimal("2.0")],
        )

    def test_bad_ordering(self):
        self.assertRaises(
            InvalidOrdering,
            LongitudinalRefsets(
                subject_identifier=self.subject_identifier,
                visit_model="edc_visit_tracking.subjectvisit",
                name="reference_app.crfone",
                reference_model_cls=Reference,
            ).order_by,
            "blah",
        )

    def test_get(self):
        refset = LongitudinalRefsets(
            subject_identifier=self.subject_identifier,
            visit_model="edc_visit_tracking.subjectvisit",
            name="reference_app.crfone",
            reference_model_cls=Reference,
        )
        self.assertEqual(refset.fieldset("field_str").all().values, ["NEG", "POS", "POS"])
        self.assertEqual(
            refset.fieldset("field_str").all().order_by("-report_datetime").values,
            ["POS", "POS", "NEG"],
        )

    def test_get2(self):
        refsets = LongitudinalRefsets(
            subject_identifier=self.subject_identifier,
            visit_model="edc_visit_tracking.subjectvisit",
            name="reference_app.crfone",
            reference_model_cls=Reference,
        )
        self.assertEqual(
            refsets.fieldset("field_str").all().order_by("field_datetime").values,
            ["NEG", "POS", "POS"],
        )
        self.assertEqual(
            refsets.fieldset("field_str").order_by("-field_datetime").all().values,
            ["POS", "POS", "NEG"],
        )

    def test_get_last(self):
        refsets = LongitudinalRefsets(
            subject_identifier=self.subject_identifier,
            visit_model="edc_visit_tracking.subjectvisit",
            name="reference_app.crfone",
            reference_model_cls=Reference,
        )
        self.assertEqual(
            refsets.fieldset("field_str").order_by("field_datetime").last(), "POS"
        )
        self.assertEqual(
            refsets.fieldset("field_str").order_by("-field_datetime").last(), "NEG"
        )

    def test_repr(self):
        refsets = LongitudinalRefsets(
            subject_identifier=self.subject_identifier,
            visit_model="edc_visit_tracking.subjectvisit",
            name="reference_app.crfone",
            reference_model_cls=Reference,
        )
        self.assertTrue(repr(refsets))
        for refset in refsets:
            self.assertTrue(repr(refset))

    def test_with_model_name(self):
        refsets = LongitudinalRefsets(
            subject_identifier=self.subject_identifier,
            visit_model="edc_visit_tracking.subjectvisit",
            name="reference_app.crfone",
            reference_model_cls="edc_reference.reference",
        )
        self.assertTrue(repr(refsets))
        for refset in refsets:
            self.assertTrue(repr(refset))
