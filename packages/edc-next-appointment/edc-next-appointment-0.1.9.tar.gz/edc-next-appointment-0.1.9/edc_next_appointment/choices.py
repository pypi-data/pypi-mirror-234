from django.utils.translation import gettext_lazy as _
from edc_constants.constants import OTHER, PATIENT

APPT_DATE_INFO_SOURCES = (
    ("health_records", _("Health record")),
    (PATIENT, _("Patient")),
    ("estimated", _("I estimated the date")),
)

MISSED_VISIT_REASONS = (
    ("forgot", _("Forgot / Can’t remember being told about appointment")),
    ("family_emergency", _("Family emergency (e.g. funeral) and was away")),
    ("travelling", _("Away travelling/visiting")),
    ("working_schooling", _("Away working/schooling")),
    ("too_sick", _("Too sick or weak to come to the centre")),
    ("lack_of_transport", _("Transportation difficulty")),
    ("NOT_SCHEDULED_FOR_FACILITY", _("Clinic visit not required for facility")),
    (OTHER, _("Other reason (specify below)")),
)
