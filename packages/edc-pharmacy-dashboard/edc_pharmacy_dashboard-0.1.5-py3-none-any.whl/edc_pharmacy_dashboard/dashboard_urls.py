from django.conf import settings

"""To customize any of the values below,
use settings.EDC_PHARMACY_DASHBOARD_URL_NAMES.
"""

dashboard_urls = {}

try:
    dashboard_urls.update(**settings.EDC_PHARMACY_DASHBOARD_URL_NAMES)
except AttributeError:
    pass
