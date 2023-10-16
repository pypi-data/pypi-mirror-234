from edc_crf.crf_form_validator import CrfFormValidator

from .form_validator_mixins import NextAppointmentFormValidatorMixin


class NextAppointmentFormValidator(NextAppointmentFormValidatorMixin, CrfFormValidator):
    def clean(self):
        self.validate_date_is_on_clinic_day()
        super().clean()
