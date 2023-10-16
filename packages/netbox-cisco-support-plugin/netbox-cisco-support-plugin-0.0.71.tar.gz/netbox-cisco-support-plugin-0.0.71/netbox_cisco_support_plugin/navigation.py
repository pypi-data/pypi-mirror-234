from extras.plugins import PluginMenuItem

menu_items = (
    PluginMenuItem(
        link="plugins:netbox_cisco_support_plugin:ciscodevicesupport_list", link_text="Cisco Device Support"
    ),
    PluginMenuItem(
        link="plugins:netbox_cisco_support_plugin:ciscodevicetypesupport_list",
        link_text="Cisco Device Type Support",
    ),
)
