from django.db import models
from edc_consent.field_mixins import PersonalFieldsMixin
from edc_consent.field_mixins.identity_fields_mixin import IdentityFieldsMixin
from edc_consent.model_mixins import ConsentModelMixin
from edc_identifier.managers import SubjectIdentifierManager
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_metadata.model_mixins.updates import UpdatesCrfMetadataModelMixin
from edc_model.models import BaseUuidModel
from edc_model.models.historical_records import HistoricalRecords
from edc_offstudy.model_mixins import OffstudyModelMixin
from edc_reference.model_mixins import ReferenceModelMixin
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_sites.models import SiteModelMixin
from edc_visit_schedule.model_mixins import OffScheduleModelMixin, OnScheduleModelMixin
from edc_visit_tracking.model_mixins import VisitTrackingCrfModelMixin
from edc_visit_tracking.models import SubjectVisit

from edc_next_appointment.model_mixins import NextAppointmentCrfModelMixin


class OnSchedule(SiteModelMixin, OnScheduleModelMixin, BaseUuidModel):
    pass


class OffSchedule(SiteModelMixin, OffScheduleModelMixin, BaseUuidModel):
    pass


class SubjectOffstudy(OffstudyModelMixin, BaseUuidModel):
    class Meta(OffstudyModelMixin.Meta):
        pass


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

    history = HistoricalRecords()

    def natural_key(self):
        return (self.subject_identifier,)  # noqa


class BaseCrfModel(
    VisitTrackingCrfModelMixin,
    SiteModelMixin,
    UpdatesCrfMetadataModelMixin,
    ReferenceModelMixin,
    models.Model,
):
    subject_visit = models.OneToOneField(
        SubjectVisit, on_delete=models.PROTECT, related_name="+"
    )

    class Meta:
        abstract = True


class CrfOne(BaseCrfModel, BaseUuidModel):
    f1 = models.CharField(max_length=50, null=True)


class NextAppointment(NextAppointmentCrfModelMixin, BaseCrfModel, BaseUuidModel):
    pass
