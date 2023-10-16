from django.utils.translation import gettext_lazy as _
from edc_constants.constants import (
    ESTIMATED,
    HOSPITAL_NOTES,
    OTHER,
    OUTPATIENT_CARDS,
    PATIENT,
    PATIENT_REPRESENTATIVE,
)

list_data = {
    "edc_next_appointment.infosources": [
        (PATIENT, _("Patient")),
        (
            PATIENT_REPRESENTATIVE,
            _("Patient representative (e.g., next of kin, relative, guardian)"),
        ),
        (HOSPITAL_NOTES, _("Hospital notes")),
        (OUTPATIENT_CARDS, _("Outpatient cards")),
        (ESTIMATED, _("Estimated by research staff")),
        (OTHER, _("Other")),
    ],
    "edc_visit_tracking.subjectvisitmissedreasons": [
        ("forgot", _("Forgot / Can’t remember being told about appointment")),
        ("family_emergency", _("Family emergency (e.g. funeral) and was away")),
        ("travelling", _("Away travelling/visiting")),
        ("working_schooling", _("Away working/schooling")),
        ("too_sick", _("Too sick or weak to come to the centre")),
        ("lack_of_transport", _("Transportation difficulty")),
        (OTHER, _("Other reason (specify below)")),
    ],
}
