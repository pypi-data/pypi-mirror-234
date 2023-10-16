from django.apps.config import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "edc_next_appointment"
    verbose_name = "Edc Next Appointment"
    has_exportable_data = False
    include_in_administration_section = False
