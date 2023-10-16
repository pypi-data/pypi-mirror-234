from django.db import models
from django.db.models.deletion import PROTECT
from edc_consent.field_mixins.identity_fields_mixin import IdentityFieldsMixin
from edc_consent.field_mixins.personal_fields_mixin import PersonalFieldsMixin
from edc_consent.model_mixins.consent_model_mixin import ConsentModelMixin
from edc_crf.model_mixins import CrfModelMixin
from edc_identifier.managers import SubjectIdentifierManager
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_lab.model_mixins import RequisitionModelMixin
from edc_model.models import BaseUuidModel
from edc_offstudy.model_mixins.offstudy_model_mixin import OffstudyModelMixin
from edc_registration.model_mixins.updates_or_creates_registered_subject_model_mixin import (
    UpdatesOrCreatesRegistrationModelMixin,
)
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow
from edc_visit_schedule.model_mixins.off_schedule_model_mixin import (
    OffScheduleModelMixin,
)
from edc_visit_schedule.model_mixins.on_schedule_model_mixin import OnScheduleModelMixin
from edc_visit_tracking.models import SubjectVisit

from edc_reference.model_mixins import (
    ReferenceModelMixin,
    RequisitionReferenceModelMixin,
)


class OnSchedule(SiteModelMixin, OnScheduleModelMixin, BaseUuidModel):
    pass


class OffSchedule(SiteModelMixin, OffScheduleModelMixin, BaseUuidModel):
    pass


class OnScheduleTwo(SiteModelMixin, OnScheduleModelMixin, BaseUuidModel):
    pass


class OffScheduleTwo(SiteModelMixin, OffScheduleModelMixin, BaseUuidModel):
    pass


class SubjectOffstudy(OffstudyModelMixin, BaseUuidModel):
    class Meta(OffstudyModelMixin.Meta):
        pass


class DeathReport(UniqueSubjectIdentifierFieldMixin, SiteModelMixin, BaseUuidModel):
    objects = SubjectIdentifierManager()

    def natural_key(self):
        return (self.subject_identifier,)


class SubjectConsent(
    ConsentModelMixin,
    PersonalFieldsMixin,
    IdentityFieldsMixin,
    UniqueSubjectIdentifierFieldMixin,
    UpdatesOrCreatesRegistrationModelMixin,
    SiteModelMixin,
    BaseUuidModel,
):
    objects = SubjectIdentifierManager()

    on_site = CurrentSiteManager()

    def natural_key(self):
        return (self.subject_identifier,)


class SubjectRequisition(
    RequisitionModelMixin,
    RequisitionReferenceModelMixin,
    BaseUuidModel,
):
    pass


class TestModel(CrfModelMixin, ReferenceModelMixin, BaseUuidModel):
    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    report_datetime = models.DateTimeField(default=get_utcnow)

    field_str = models.CharField(max_length=50)


class TestModelBad(CrfModelMixin, BaseUuidModel):
    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    report_datetime = models.DateTimeField(default=get_utcnow)

    field_str = models.CharField(max_length=50)


class CrfOne(CrfModelMixin, ReferenceModelMixin, BaseUuidModel):
    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    report_datetime = models.DateTimeField(default=get_utcnow)

    field_str = models.CharField(max_length=50)

    field_date = models.DateField(null=True)

    field_datetime = models.DateTimeField(null=True)

    field_int = models.IntegerField(null=True)


class CrfWithBadField(CrfModelMixin, ReferenceModelMixin, BaseUuidModel):
    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    report_datetime = models.DateTimeField(default=get_utcnow)

    field_str = models.CharField(max_length=50)

    field_date = models.DateField(null=True)

    field_datetime = models.DateTimeField(null=True)

    field_int = models.IntegerField(null=True)


class CrfWithDuplicateField(CrfModelMixin, ReferenceModelMixin, BaseUuidModel):
    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    report_datetime = models.DateTimeField(default=get_utcnow)

    field_str = models.CharField(max_length=50)

    field_date = models.DateField(null=True)

    field_datetime = models.DateTimeField(null=True)

    field_int = models.IntegerField(null=True)


class CrfWithUnknownDatatype(CrfModelMixin, ReferenceModelMixin, BaseUuidModel):
    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    report_datetime = models.DateTimeField(default=get_utcnow)

    field_decimal = models.DecimalField(decimal_places=2, max_digits=10)


class CrfOneProxyOne(CrfOne):
    class Meta:
        proxy = True


class CrfOneProxyTwo(CrfOne):
    class Meta:
        proxy = True
