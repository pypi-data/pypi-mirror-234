from extras.plugins import PluginConfig
from .version import __version__


class CiscoSupportConfig(PluginConfig):
    name = "netbox_cisco_support_plugin"
    verbose_name = "Cisco Support Plugin"
    description = "Cisco device support, device type support, and software release information with the Cisco support APIs"
    version = __version__
    author = "Willi Kubny"
    author_email = "willi.kubny@gmail.com"
    base_url = "cisco-support"
    min_version = "3.5.0"
    required_settings = ["CISCO_SUPPORT_API_CLIENT_ID", "CISCO_SUPPORT_API_CLIENT_SECRET"]
    default_settings = {"MANUFACTURER": "Cisco", "TEMPLATE_EXTENSION_PLACEMENT": "right"}


config = CiscoSupportConfig
