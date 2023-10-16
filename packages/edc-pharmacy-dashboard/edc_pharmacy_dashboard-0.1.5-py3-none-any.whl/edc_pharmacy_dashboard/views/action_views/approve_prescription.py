from django.apps import apps as django_apps
from django.contrib import messages

# from edc_pharmacy.medications import PrescriptionApprovalValidator, \
#     PrescriptionApprovalValidatorError

from .base_action_view import BaseActionView


app_config = django_apps.get_app_config("edc_pharmacy_dashboard")
edc_pharma_app_config = django_apps.get_app_config("edc_pharma")


class ApprovedPrescription(object):
    pass


class ApprovedPrescriptionError(Exception):
    pass


class ApprovePrescriptionView(BaseActionView):

    post_url_name = app_config.listboard_url_name
    listboard_url_name = app_config.prescription_listboard_url_name
    valid_form_actions = ["approve_selected_prescription"]
    prescription_model = django_apps.get_model(
        *edc_pharma_app_config.prescription_model.split(".")
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._selected_manifest = None

    def process_form_action(self):
        if not self.selected_items:
            message = "Nothing to do. No items have been selected."
            messages.warning(self.request, message)
        elif self.action == "approve_selected_prescriptions":
            count = 0
            for selected_item in self.selected_items:
                prescription = self.prescription_model_cls.objects.get(pk=selected_item)
                try:
                    ApprovedPrescription(prescription=prescription)
                except ApprovedPrescriptionError as e:
                    messages.error(self.request, str(e))
                    break
                else:
                    count += 1
            if count:
                messages.success(
                    self.request,
                    f"{count}/{len(self.selected_items)} items have been approved.",
                )
