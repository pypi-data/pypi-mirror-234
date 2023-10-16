from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar

no_url_namespace = True if settings.APP_NAME == "edc_pharmacy_dashboard" else False

navbar = Navbar(name="pharmacy_dashboard")


navbar.append_item(
    NavbarItem(
        name="prescribe",
        title="prescribe",
        label="Prescribe",
        glyphicon="glyphicon-edit",
        no_url_namespace=no_url_namespace,
        codename="edc_navbar.nav_pharmacy_prescribe",
        url_name="edc_pharmacy_dashboard:prescribe_listboard_url",
    )
)

navbar.append_item(
    NavbarItem(
        name="dispense",
        title="dispense",
        label="Dispense",
        glyphicon="glyphicon-share",
        no_url_namespace=no_url_namespace,
        codename="edc_navbar.nav_pharmacy_dispense",
        url_name="edc_pharmacy_dashboard:dispense_listboard_url",
    )
)

navbar.append_item(
    NavbarItem(
        name="pharmacy",
        fa_icon="fa-medkit",
        no_url_namespace=no_url_namespace,
        codename="edc_navbar.nav_pharmacy_section",
        url_name="edc_pharmacy_dashboard:home_url",
    )
)


site_navbars.register(navbar)
