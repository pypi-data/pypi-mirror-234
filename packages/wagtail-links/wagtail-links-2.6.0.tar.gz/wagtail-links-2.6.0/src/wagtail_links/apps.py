from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WagtailLinksConfig(AppConfig):
    name = "wagtail_links"
    # Translators: Backend Library Name
    verbose_name = _("Wagtail Links")
