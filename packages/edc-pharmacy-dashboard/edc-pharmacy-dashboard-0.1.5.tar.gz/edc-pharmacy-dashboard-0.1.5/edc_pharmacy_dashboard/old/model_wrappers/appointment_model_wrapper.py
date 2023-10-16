from django.apps import apps as django_apps
from edc_model_wrapper import ModelWrapper

# from edc_pharmacy import AppointmentDescriber
# from edc_pharmacy.models import Prescription


app_config = django_apps.get_app_config("edc_pharmacy_dashboard")
# edc_pharma_app_config = django_apps.get_app_config('edc_pharmacy')


class AppointmentModelWrapper(ModelWrapper):

    model = "edc_pharmacy.dispenseappointment"
    next_url_name = app_config.appointment_listboard_url_name
    querystring_attrs = ["subject_identifier"]
    prescription_model = "edc_pharmacy.prescription"

    @property
    def dispense_appt_describe(self):
        return None
        # return AppointmentDescriber(dispense_appointment=self.object)

    @property
    def subject_identifier(self):
        return self.object.subject_identifier

    @property
    def prescriptions(self):
        model_cls = django_apps.get_model(self.prescription_model)
        return model_cls.objects.filter(dispense_appointment=self.object)

    @property
    def appointment_id(self):
        return str(self.object.id)

    @property
    def can_dispense_labels(self):
        if self.object.previous():
            return self.object.previous().is_dispensed
        return True
