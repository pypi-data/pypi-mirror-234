from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from edc_dashboard.view_mixins import EdcViewMixin
from edc_navbar import NavbarViewMixin

app_config = django_apps.get_app_config("edc_pharmacy_dashboard")


class HomeView(EdcViewMixin, NavbarViewMixin, TemplateView):

    template_name = "edc_pharmacy_dashboard/home.html"
    base_template_name = app_config.base_template_name or "edc_dashboard/base.html"
    navbar_name = "pharmacy_dashboard"
    navbar_selected_item = "pharmacy"
    app_config_name = "edc_pharmacy_dashboard"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            prescribe_listboard_url_name=app_config.prescribe_listboard_url_name,
            dispense_listboard_url_name=app_config.dispense_listboard_url_name,
        )
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
