from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin

from edc_next_appointment.form_validators import NextAppointmentFormValidator
from edc_next_appointment.modelform_mixins import NextAppointmentModelFormMixin

from .models import NextAppointment


class NextAppointmentForm(NextAppointmentModelFormMixin, CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = NextAppointmentFormValidator

    def validate_against_consent(self) -> None:
        pass

    class Meta:
        model = NextAppointment
        fields = "__all__"
