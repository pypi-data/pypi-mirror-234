from edc_auth.site_auths import site_auths
from edc_auth.utils import remove_default_model_permissions_from_edc_permissions

site_auths.add_post_update_func(
    "edc_pharmacy_dashboard", remove_default_model_permissions_from_edc_permissions
)
