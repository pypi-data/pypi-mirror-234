from django.apps import apps as django_apps


edc_pharmacy_app_config = django_apps.get_app_config("edc_pharmacy")


class ModelsViewMixin:
    @property
    def dispense_model(self):
        return django_apps.get_model(
            *edc_pharmacy_app_config.requisition_model.split(".")
        )
