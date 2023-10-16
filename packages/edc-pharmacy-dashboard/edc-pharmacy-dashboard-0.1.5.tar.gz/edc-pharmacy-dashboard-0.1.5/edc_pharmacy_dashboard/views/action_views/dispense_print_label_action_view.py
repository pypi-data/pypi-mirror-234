from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.utils.decorators import method_decorator

# from edc_pharmacy.dispense import Dispense

from ..dispense_print_label_mixin import DispensePrintLabelMixin
from .base_action_view import BaseActionView


app_config = django_apps.get_app_config("edc_pharmacy_dashboard")


class DispensePrintLabelActionView(DispensePrintLabelMixin, BaseActionView):

    post_url_name = app_config.appointment_listboard_url_name
    valid_form_actions = ["print_labels"]
    action_name = "pharma"

    # dispense_cls = Dispense

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.print_labels(request, **kwargs)
        return HttpResponseRedirect(self.post_url)
