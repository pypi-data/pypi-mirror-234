from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

next_appointment_app_admin = EdcAdminSite(
    name="next_appointment_app_admin", app_label=AppConfig.name
)
