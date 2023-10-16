# coding=utf-8
from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "edc_pharmacy_dashboard"
    verbose_name = "Pharmacy Dashboard"
    include_in_administration_section = False
    admin_site_name = "edc_pharmacy_admin"
    template_path = "edc_pharmacy_dashboard"
    url_namespace = "edc_pharmacy_dashboard"
    dashboard_name = "edc_pharmacy_dashboard"
    base_template_name = "edc_dashboard/base.html"

    dashboard_url_name = f"{url_namespace}:home_url"
    home_url_name = f"{url_namespace}:home_url"
    listboard_url_name = f"{url_namespace}:prescription_listboard_url"

    # dispensing_form_url_name = f'{url_namespace}:dispensing_form_url'
    dispense_listboard_url_name = f"{url_namespace}:dispense_listboard_url"

    prescribe_listboard_template_name = f"{template_path}/prescription_listboard.html"
    prescribe_listboard_url_name = f"{url_namespace}:prescribe_listboard_url"


#     worklist_listboard_template_name = f'{template_path}/worklist_listboard.html'
#     worklist_listboard_url_name = f'{url_namespace}:worklist_listboard_url'
#     appointment_listboard_template_name = f'{template_path}/appointment_listboard.html'
#     appointment_listboard_url_name = f'{url_namespace}:appointment_listboard_url'
#     dispense_print_label_action_url_name = f'{url_namespace}:dispense_print_label_action_url'
