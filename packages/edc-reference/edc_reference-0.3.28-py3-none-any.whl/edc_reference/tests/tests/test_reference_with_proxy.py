from django.contrib.sites.models import Site
from edc_lab.models.panel import Panel
from edc_lab_panel.constants import CD4, FBC, VL
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.models import SubjectVisit

from edc_reference.models import Reference
from edc_reference.reference import ReferenceGetter, ReferenceUpdater
from reference_app.models import CrfOne, CrfOneProxyOne
from reference_app.register_reference_configs import register_reference_configs
from reference_app.visit_schedules import visit_schedule2

from .test_case import TestCase


class TestReferenceModel(TestCase):
    def setUp(self):
        self.panel_cd4 = Panel.objects.get(name=CD4)
        self.panel_vl = Panel.objects.get(name=VL)
        self.panel_fbc = Panel.objects.get(name=FBC)
        self.site = Site.objects.get_current()
        site_visit_schedules._registry = {}
        site_visit_schedules.register(visit_schedule2)
        register_reference_configs()
        self.prepare_subject_visit("reference_app.onscheduletwo")

    def test_with_proxy(self):
        self.subject_visit = SubjectVisit.objects.get(
            visit_code="1000", visit_schedule_name="visit_schedule2"
        )

        model_obj = CrfOne.objects.create(subject_visit=self.subject_visit, field_str="erik")
        ReferenceUpdater(model_obj=model_obj)
        reference = Reference.objects.get(
            identifier=self.subject_identifier,
            timepoint=self.subject_visit.timepoint,
            field_name="field_str",
        )
        self.assertEqual(reference.value, "erik")

        model_obj = CrfOneProxyOne.objects.create(
            subject_visit=self.subject_visit, field_str="bob"
        )
        ReferenceUpdater(model_obj=model_obj)
        reference = ReferenceGetter(field_name="field_str", model_obj=model_obj)
        self.assertEqual(reference.value, "bob")
