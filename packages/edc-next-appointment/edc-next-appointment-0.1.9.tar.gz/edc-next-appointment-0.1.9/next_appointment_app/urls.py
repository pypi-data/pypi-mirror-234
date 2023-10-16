from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from edc_utils.paths_for_urlpatterns import paths_for_urlpatterns

from .admin_site import next_appointment_app_admin
from .views import SubjectDashboardView

app_name = "next_appointment_app"

urlpatterns = SubjectDashboardView.urls(app_name, label="subject_dashboard")

urlpatterns += [
    *paths_for_urlpatterns("edc_next_appointment"),
    path("data_manager_app/admin/", next_appointment_app_admin.urls),
    path("/admin", admin.site.urls),
    path("", RedirectView.as_view("/admin"), name="home_url"),
    path("", RedirectView.as_view("/admin"), name="administration_url"),
]
