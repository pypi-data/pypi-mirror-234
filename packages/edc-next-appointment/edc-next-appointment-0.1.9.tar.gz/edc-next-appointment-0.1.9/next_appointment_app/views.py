from edc_subject_dashboard.views import SubjectDashboardView as BaseSubjectDashboardView


class SubjectDashboardView(BaseSubjectDashboardView):
    consent_model = "next_appointment_app.subjectconsent"
    navbar_name = "next_appointment_app"
    visit_model = "next_appointment_app.subjectvisit"

    def get_navbar_context_data(self, context):
        return context
