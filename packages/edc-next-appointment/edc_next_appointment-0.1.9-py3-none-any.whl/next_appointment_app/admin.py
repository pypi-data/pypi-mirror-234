from django.contrib import admin
from edc_model_admin.dashboard import (
    ModelAdminCrfDashboardMixin,
    ModelAdminSubjectDashboardMixin,
)

from .admin_site import next_appointment_app_admin
from .models import CrfOne, OffSchedule, OnSchedule, SubjectConsent, SubjectVisit


@admin.register(OnSchedule, site=next_appointment_app_admin)
class OnScheduleAdmin(ModelAdminSubjectDashboardMixin, admin.ModelAdmin):
    pass


@admin.register(OffSchedule, site=next_appointment_app_admin)
class OffScheduleAdmin(ModelAdminSubjectDashboardMixin, admin.ModelAdmin):
    pass


@admin.register(SubjectConsent, site=next_appointment_app_admin)
class SubjectConsentAdmin(ModelAdminSubjectDashboardMixin, admin.ModelAdmin):
    pass


@admin.register(SubjectVisit, site=next_appointment_app_admin)
class SubjectVisitAdmin(ModelAdminSubjectDashboardMixin, admin.ModelAdmin):
    pass


@admin.register(CrfOne, site=next_appointment_app_admin)
class CrfOneAdmin(ModelAdminCrfDashboardMixin, admin.ModelAdmin):
    show_save_next = True
    show_cancel = True
