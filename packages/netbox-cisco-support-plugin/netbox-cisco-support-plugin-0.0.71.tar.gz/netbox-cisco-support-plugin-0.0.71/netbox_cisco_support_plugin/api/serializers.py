from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from dcim.api.serializers import NestedDeviceTypeSerializer, NestedDeviceSerializer
from ..models import CiscoDeviceTypeSupport, CiscoDeviceSupport


#### Regular Serializers #####################################################################################


class CiscoDeviceTypeSupportSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_cisco_support_plugin-api:ciscodevicetypesupport-detail"
    )

    device_type = NestedDeviceTypeSerializer()

    class Meta:
        model = CiscoDeviceTypeSupport
        # fmt: off
        fields = [
            "id", "url", "display", "name", "device_type", "pid", "eox_has_error", "eox_error",
            "eox_announcement_date", "end_of_sale_date", "end_of_sw_maintenance_releases",
            "end_of_security_vul_support_date", "end_of_routine_failure_analysis_date",
            "end_of_service_contract_renewal", "last_date_of_support", "end_of_svc_attach_date",
            "tags", "custom_fields", "created", "last_updated",
        ]
        # fmt: on


class CiscoDeviceSupportSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_cisco_support_plugin-api:ciscodevicesupport-detail"
    )

    device = NestedDeviceSerializer()

    class Meta:
        model = CiscoDeviceSupport
        # fmt: off
        fields = [
            "id", "url", "display", "name", "device", "pid", "serial", "api_status", "sr_no_owner",
            "is_covered", "coverage_end_date", "contract_supplier", "service_line_descr",
            "service_contract_number", "warranty_end_date", "warranty_type", "partner_status",
            "partner_service_level", "partner_customer_number", "partner_coverage_end_date",
            "recommended_release", "desired_release", "current_release", "desired_release_status",
            "current_release_status", "eox_has_error", "eox_error", "eox_announcement_date",
            "end_of_sale_date", "end_of_sw_maintenance_releases", "end_of_security_vul_support_date",
            "end_of_routine_failure_analysis_date", "end_of_service_contract_renewal",
            "last_date_of_support", "end_of_svc_attach_date", "tags", "custom_fields", "created",
            "last_updated",
        ]
        # fmt: on
