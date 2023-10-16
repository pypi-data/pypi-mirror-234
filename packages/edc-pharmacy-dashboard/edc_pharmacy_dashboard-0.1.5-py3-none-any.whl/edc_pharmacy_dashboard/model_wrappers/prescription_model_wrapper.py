from django.apps import apps as django_apps
from edc_model_wrapper import ModelWrapper


app_config = django_apps.get_app_config("edc_pharmacy_dashboard")


class PrescriptionModelWrapper(ModelWrapper):

    model = "edc_pharmacy.prescription"
    next_url_name = app_config.prescribe_listboard_url_name
    querystring_attrs = ["subject_identifier"]

    @property
    def dispense_appt_describe(self):
        return None

    @property
    def subject_identifier(self):
        return self.object.subject_identifier

    @property
    def is_pending(self):
        return (
            self.dispense_appt_describe.is_next_pending_appointment()
            and not self.object.is_approved
        )
