|pypi| |actions| |codecov| |downloads|

edc-next-appointment
--------------------

Base classes for managing next appointment CRF at each timepoint

Declare in your app as a longitudinal model / CRF.

For example:

.. code-block:: python

    # model.py
    class NextAppointment(NextAppointmentCrfModelMixin, CrfModelMixin, BaseUuidModel):

        class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
            verbose_name = "Next Appointment"
            verbose_name_plural = "Next Appointments"


    # forms.py
    class NextAppointmentForm(NextAppointmentModelFormMixin, CrfModelFormMixin, forms.ModelForm):
        form_validator_cls = NextAppointmentFormValidator

        class Meta:
            model = NextAppointment
            fields = "__all__"


    # admin.py
    @admin.register(NextAppointment, site=intecomm_subject_admin)
    class NextAppointmentAdmin(NextAppointmentModelAdminMixin, CrfModelAdmin):
        form = NextAppointmentForm



.. |pypi| image:: https://img.shields.io/pypi/v/edc-next-appointment.svg
    :target: https://pypi.python.org/pypi/edc-next-appointment

.. |actions| image:: https://github.com/clinicedc/edc-next-appointment/workflows/build/badge.svg?branch=develop
  :target: https://github.com/clinicedc/edc-next-appointment/actions?query=workflow:build

.. |codecov| image:: https://codecov.io/gh/clinicedc/edc-next-appointment/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/clinicedc/edc-next-appointment

.. |downloads| image:: https://pepy.tech/badge/edc-next-appointment
   :target: https://pepy.tech/project/edc-next-appointment
