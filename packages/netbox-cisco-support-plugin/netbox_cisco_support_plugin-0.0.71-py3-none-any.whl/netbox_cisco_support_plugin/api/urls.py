from netbox.api.routers import NetBoxRouter
from . import views


app_name = "netbox_cisco_support_plugin"

router = NetBoxRouter()
router.register(r"device", views.CiscoDeviceSupportViewSet)
router.register(r"device-type", views.CiscoDeviceTypeSupportViewSet)

urlpatterns = router.urls
