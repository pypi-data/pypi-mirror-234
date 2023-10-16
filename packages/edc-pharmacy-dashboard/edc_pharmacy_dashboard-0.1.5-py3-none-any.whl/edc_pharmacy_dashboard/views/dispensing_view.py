from django import forms
from django.apps import apps as django_apps
from django.contrib import messages
from django.core.management.color import color_style
from django.forms.forms import Form
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from edc_dashboard.view_mixins import EdcViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView

style = color_style()


class Dispense:
    def __init__(self, **kwargs):
        pass


class DispenseForm(Form):

    medications = forms.MultipleChoiceField()


app_config = django_apps.get_app_config("edc_pharmacy_dashboard")


# class DispenseViewMixin(DispensePrintLabelMixin):
class DispenseViewMixin:

    dispense_cls = Dispense
    prescription_model = "edc_pharmacy.prescription"

    def get_success_url(self):
        return "/"

    def post(self, request, *args, **kwargs):
        subject_identifier = kwargs.get("subject_identifier")
        prescriptions = []

        error_message = None
        for key in self.request.POST:
            if key.startswith("med"):
                p = self.prescription_model_cls.objects.get(
                    id=self.request.POST.get(key)
                )
                if not p.dispense_appointment.is_dispensed:
                    error_message = "Dispensing is required before printing labels."
                    break
                prescriptions.append(p)
        if not error_message:
            action = self.request.POST.get("action")
            dispense = self.dispense_cls(
                prescriptions=prescriptions, action=action)
            if dispense.printed_labels:
                for label in dispense.printed_labels:
                    medication = label.get("medication")
                    subject_identifier = label.get("subject_identifier")
                    msg = f" Printed {medication} for {subject_identifier}."
                    messages.add_message(request, messages.SUCCESS, msg)
            else:
                msg = f"Nothing selected for {subject_identifier} FFFF."
                messages.add_message(request, messages.ERROR, msg)
        else:
            messages.add_message(request, messages.WARNING, error_message)
        url = reverse(
            app_config.appointment_listboard_url_name,
            kwargs={"subject_identifier": subject_identifier},
        )
        return HttpResponseRedirect(url)

    @property
    def prescription_model_cls(self):
        return django_apps.get_model(self.prescription_model)


class DispensingView(DispenseViewMixin, EdcViewMixin, BaseDashboardView):
    app_config_name = "edc_pharmacy"
    dashboard_url_name = "subject_dashboard_url"
