from datetime import date
from django.db import models
from django.urls import reverse
from netbox.models import ChangeLoggedModel
from utilities.querysets import RestrictedQuerySet
from dcim.models import Device, DeviceType


class CiscoDeviceTypeSupport(ChangeLoggedModel):
    objects = RestrictedQuerySet.as_manager()

    device_type = models.OneToOneField(
        to="dcim.DeviceType", on_delete=models.CASCADE, verbose_name="Device Type"
    )

    def __str__(self):
        return f"{self.device_type}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_cisco_support_plugin:ciscodevicetypesupport_list")

    def save(self, *args, **kwargs):
        # Query the DeviceType model
        device_type_obj = DeviceType.objects.select_related().get(id=self.device_type.id)
        # Set the name from the DeviceType model
        self.name = device_type_obj.model
        # Set the pid from the DeviceType part_number
        self.pid = device_type_obj.part_number

        # Call the "real" save() method
        super().save(*args, **kwargs)

    #### Fileds same as dcim.DeviceType #####################################################################
    # Create these fields again because referencing them from the dcim.device model was not working

    # Field get set in custom save() function
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Name")

    # Field get set in custom save() function
    pid = models.CharField(max_length=100, blank=True, null=True, verbose_name="PID")

    #### Fileds for CiscoDeviceTypeSupport ##################################################################

    eox_has_error = models.BooleanField(default=False, verbose_name="Has EoX Error")

    eox_error = models.CharField(max_length=100, blank=True, null=True, verbose_name="EoX Error")

    eox_announcement_date = models.DateField(blank=True, null=True, verbose_name="EoX Announcement Date")

    end_of_sale_date = models.DateField(blank=True, null=True, verbose_name="End of Sale Date")

    end_of_sw_maintenance_releases = models.DateField(
        blank=True, null=True, verbose_name="End of Sw-Maint. Date"
    )

    end_of_security_vul_support_date = models.DateField(
        blank=True, null=True, verbose_name="End of Sec-Vul. Date"
    )

    end_of_routine_failure_analysis_date = models.DateField(
        blank=True, null=True, verbose_name="End of Routine-Fail. Analysis Date"
    )

    end_of_service_contract_renewal = models.DateField(
        blank=True, null=True, verbose_name="End of Service Cont. Renewal"
    )

    end_of_svc_attach_date = models.DateField(blank=True, null=True, verbose_name="End of Svc-Attach. Date")

    last_date_of_support = models.DateField(blank=True, null=True, verbose_name="Last Date of Support")

    #### Property Fileds for CiscoDeviceTypeSupport #########################################################

    # Property field for end of sales date progress bar
    @property
    def end_of_sale_total(self):
        """
        Total days until EoX. Return None if end_of_sale_date not defined.
        """
        if self.eox_announcement_date and self.end_of_sale_date:
            delta = self.end_of_sale_date - self.eox_announcement_date
            return delta.days

    # Property field for end of sales date progress bar
    @property
    def end_of_sale_remaining(self):
        """
        How many days are remaining. Return None if end_of_sale not defined.
        """
        if self.eox_announcement_date and self.end_of_sale_date:
            delta = self.end_of_sale_date - date.today()
            return delta.days
        return None

    # Property field for end of sales date progress bar
    @property
    def end_of_sale_elapsed(self):
        """
        How many days are elaped. Return None if end_of_sale not defined.
        """
        if self.eox_announcement_date and self.end_of_sale_date:
            return self.end_of_sale_total - self.end_of_sale_remaining
        return None

    # Property field for end of sales date progress bar
    @property
    def end_of_sale_progress(self):
        """
        Coverage progress in percent. Return None if coverage_end_date not defined.
        """
        if self.eox_announcement_date and self.end_of_sale_date:
            return round(self.end_of_sale_elapsed / self.end_of_sale_total * 100)
        return None

    # Property field for end of sales date progress bar
    @property
    def end_of_sale_progress_bar_class(self):
        """
        Coverage progress bar class.
        """
        if self.eox_announcement_date and self.end_of_sale_date:
            if self.end_of_sale_remaining < 60:
                return "bg-danger"
            if self.end_of_sale_remaining < 365:
                return "bg-warning"
        return "bg-success"

    # Property field for end of software maintenance date progress bar
    @property
    def end_of_sw_maintenance_releases_total(self):
        """
        Total days until EoX. Return None if end_of_sale_date not defined.
        """
        if self.eox_announcement_date and self.end_of_sw_maintenance_releases:
            delta = self.end_of_sw_maintenance_releases - self.eox_announcement_date
            return delta.days

    # Property field for end of software maintenance date progress bar
    @property
    def end_of_sw_maintenance_releases_remaining(self):
        """
        How many days are remaining. Return None if end_of_sale not defined.
        """
        if self.eox_announcement_date and self.end_of_sw_maintenance_releases:
            delta = self.end_of_sw_maintenance_releases - date.today()
            return delta.days
        return None

    # Property field for end of software maintenance date progress bar
    @property
    def end_of_sw_maintenance_releases_elapsed(self):
        """
        How many days are elaped. Return None if end_of_sale not defined.
        """
        if self.eox_announcement_date and self.end_of_sw_maintenance_releases:
            return self.end_of_sw_maintenance_releases_total - self.end_of_sw_maintenance_releases_remaining
        return None

    # Property field for end of software maintenance date progress bar
    @property
    def end_of_sw_maintenance_releases_progress(self):
        """
        Coverage progress in percent. Return None if coverage_end_date not defined.
        """
        if self.eox_announcement_date and self.end_of_sw_maintenance_releases:
            return round(
                self.end_of_sw_maintenance_releases_elapsed / self.end_of_sw_maintenance_releases_total * 100
            )
        return None

    # Property field for end of software maintenance date progress bar
    @property
    def end_of_sw_maintenance_releases_progress_bar_class(self):
        """
        Coverage progress bar class.
        """
        if self.eox_announcement_date and self.end_of_sw_maintenance_releases:
            if self.end_of_sw_maintenance_releases_remaining < 60:
                return "bg-danger"
            if self.end_of_sw_maintenance_releases_remaining < 365:
                return "bg-warning"
        return "bg-success"

    # Property field for end of security vulnerability support date progress bar
    @property
    def end_of_security_vul_support_date_total(self):
        """
        Total days until EoX. Return None if end_of_sale_date not defined.
        """
        if self.eox_announcement_date and self.end_of_security_vul_support_date:
            delta = self.end_of_security_vul_support_date - self.eox_announcement_date
            return delta.days

    # Property field for end of security vulnerability support date progress bar
    @property
    def end_of_security_vul_support_date_remaining(self):
        """
        How many days are remaining. Return None if end_of_sale not defined.
        """
        if self.eox_announcement_date and self.end_of_security_vul_support_date:
            delta = self.end_of_security_vul_support_date - date.today()
            return delta.days
        return None

    # Property field for end of security vulnerability support date progress bar
    @property
    def end_of_security_vul_support_date_elapsed(self):
        """
        How many days are elaped. Return None if end_of_sale not defined.
        """
        if self.eox_announcement_date and self.end_of_security_vul_support_date:
            return (
                self.end_of_security_vul_support_date_total - self.end_of_security_vul_support_date_remaining
            )
        return None

    # Property field for end of security vulnerability support date progress bar
    @property
    def end_of_security_vul_support_date_progress(self):
        """
        Coverage progress in percent. Return None if coverage_end_date not defined.
        """
        if self.eox_announcement_date and self.end_of_security_vul_support_date:
            return round(
                self.end_of_security_vul_support_date_elapsed
                / self.end_of_security_vul_support_date_total
                * 100
            )
        return None

    # Property field for end of security vulnerability support date progress bar
    @property
    def end_of_security_vul_support_date_progress_bar_class(self):
        """
        Coverage progress bar class.
        """
        if self.eox_announcement_date and self.end_of_security_vul_support_date:
            if self.end_of_security_vul_support_date_remaining < 60:
                return "bg-danger"
            if self.end_of_security_vul_support_date_remaining < 365:
                return "bg-warning"
        return "bg-success"

    # Property field for end of routine failure analysis date progress bar
    @property
    def end_of_routine_failure_analysis_date_total(self):
        """
        Total days until EoX. Return None if end_of_sale_date not defined.
        """
        if self.eox_announcement_date and self.end_of_routine_failure_analysis_date:
            delta = self.end_of_routine_failure_analysis_date - self.eox_announcement_date
            return delta.days

    # Property field for end of routine failure analysis date progress bar
    @property
    def end_of_routine_failure_analysis_date_remaining(self):
        """
        How many days are remaining. Return None if end_of_sale not defined.
        """
        if self.eox_announcement_date and self.end_of_routine_failure_analysis_date:
            delta = self.end_of_routine_failure_analysis_date - date.today()
            return delta.days
        return None

    # Property field for end of routine failure analysis date progress bar
    @property
    def end_of_routine_failure_analysis_date_elapsed(self):
        """
        How many days are elaped. Return None if end_of_sale not defined.
        """
        if self.eox_announcement_date and self.end_of_routine_failure_analysis_date:
            return (
                self.end_of_routine_failure_analysis_date_total
                - self.end_of_routine_failure_analysis_date_remaining
            )
        return None

    # Property field for end of routine failure analysis date progress bar
    @property
    def end_of_routine_failure_analysis_date_progress(self):
        """
        Coverage progress in percent. Return None if coverage_end_date not defined.
        """
        if self.eox_announcement_date and self.end_of_routine_failure_analysis_date:
            return round(
                self.end_of_routine_failure_analysis_date_elapsed
                / self.end_of_routine_failure_analysis_date_total
                * 100
            )
        return None

    # Property field for end of routine failure analysis date progress bar
    @property
    def end_of_routine_failure_analysis_date_progress_bar_class(self):
        """
        Coverage progress bar class.
        """
        if self.eox_announcement_date and self.end_of_routine_failure_analysis_date:
            if self.end_of_routine_failure_analysis_date_remaining < 60:
                return "bg-danger"
            if self.end_of_routine_failure_analysis_date_remaining < 365:
                return "bg-warning"
        return "bg-success"

    # Property field for end of service contract renewal date progress bar
    @property
    def end_of_service_contract_renewal_total(self):
        """
        Total days until EoX. Return None if end_of_sale_date not defined.
        """
        if self.eox_announcement_date and self.end_of_service_contract_renewal:
            delta = self.end_of_service_contract_renewal - self.eox_announcement_date
            return delta.days

    # Property field for end of service contract renewal date progress bar
    @property
    def end_of_service_contract_renewal_remaining(self):
        """
        How many days are remaining. Return None if end_of_sale not defined.
        """
        if self.eox_announcement_date and self.end_of_service_contract_renewal:
            delta = self.end_of_service_contract_renewal - date.today()
            return delta.days
        return None

    # Property field for end of service contract renewal date progress bar
    @property
    def end_of_service_contract_renewal_elapsed(self):
        """
        How many days are elaped. Return None if end_of_sale not defined.
        """
        if self.eox_announcement_date and self.end_of_service_contract_renewal:
            return self.end_of_service_contract_renewal_total - self.end_of_service_contract_renewal_remaining
        return None

    # Property field for end of service contract renewal date progress bar
    @property
    def end_of_service_contract_renewal_progress(self):
        """
        Coverage progress in percent. Return None if coverage_end_date not defined.
        """
        if self.eox_announcement_date and self.end_of_service_contract_renewal:
            return round(
                self.end_of_service_contract_renewal_elapsed
                / self.end_of_service_contract_renewal_total
                * 100
            )
        return None

    # Property field for end of service contract renewal date progress bar
    @property
    def end_of_service_contract_renewal_progress_bar_class(self):
        """
        Coverage progress bar class.
        """
        if self.eox_announcement_date and self.end_of_service_contract_renewal:
            if self.end_of_service_contract_renewal_remaining < 60:
                return "bg-danger"
            if self.end_of_service_contract_renewal_remaining < 365:
                return "bg-warning"
        return "bg-success"

    # Property field for end of svc attach date progress bar
    @property
    def end_of_svc_attach_date_total(self):
        """
        Total days until EoX. Return None if end_of_sale_date not defined.
        """
        if self.eox_announcement_date and self.end_of_svc_attach_date:
            delta = self.end_of_svc_attach_date - self.eox_announcement_date
            return delta.days

    # Property field for end of svc attach date progress bar
    @property
    def end_of_svc_attach_date_remaining(self):
        """
        How many days are remaining. Return None if end_of_sale not defined.
        """
        if self.eox_announcement_date and self.end_of_svc_attach_date:
            delta = self.end_of_svc_attach_date - date.today()
            return delta.days
        return None

    # Property field for end of svc attach date progress bar
    @property
    def end_of_svc_attach_date_elapsed(self):
        """
        How many days are elaped. Return None if end_of_sale not defined.
        """
        if self.eox_announcement_date and self.end_of_svc_attach_date:
            return self.end_of_svc_attach_date_total - self.end_of_svc_attach_date_remaining
        return None

    # Property field for end of svc attach date progress bar
    @property
    def end_of_svc_attach_date_progress(self):
        """
        Coverage progress in percent. Return None if coverage_end_date not defined.
        """
        if self.eox_announcement_date and self.end_of_svc_attach_date:
            return round(self.end_of_svc_attach_date_elapsed / self.end_of_svc_attach_date_total * 100)
        return None

    # Property field for end of svc attach date progress bar
    @property
    def end_of_svc_attach_date_progress_bar_class(self):
        """
        Coverage progress bar class.
        """
        if self.eox_announcement_date and self.end_of_svc_attach_date:
            if self.end_of_svc_attach_date_remaining < 60:
                return "bg-danger"
            if self.end_of_svc_attach_date_remaining < 365:
                return "bg-warning"
        return "bg-success"

    # Property field for last day of support progress bar
    @property
    def last_date_of_support_total(self):
        """
        Total days until EoX. Return None if end_of_sale_date not defined.
        """
        if self.eox_announcement_date and self.last_date_of_support:
            delta = self.last_date_of_support - self.eox_announcement_date
            return delta.days

    # Property field for last day of support progress bar
    @property
    def last_date_of_support_remaining(self):
        """
        How many days are remaining. Return None if end_of_sale not defined.
        """
        if self.eox_announcement_date and self.last_date_of_support:
            delta = self.last_date_of_support - date.today()
            return delta.days
        return None

    # Property field for last day of support progress bar
    @property
    def last_date_of_support_elapsed(self):
        """
        How many days are elaped. Return None if end_of_sale not defined.
        """
        if self.eox_announcement_date and self.last_date_of_support:
            return self.last_date_of_support_total - self.last_date_of_support_remaining
        return None

    # Property field for last day of support progress bar
    @property
    def last_date_of_support_progress(self):
        """
        Coverage progress in percent. Return None if coverage_end_date not defined.
        """
        if self.eox_announcement_date and self.last_date_of_support:
            return round(self.last_date_of_support_elapsed / self.last_date_of_support_total * 100)
        return None

    # Property field for last day of support progress bar
    @property
    def last_date_of_support_progress_bar_class(self):
        """
        Coverage progress bar class.
        """
        if self.eox_announcement_date and self.last_date_of_support:
            if self.last_date_of_support_remaining < 60:
                return "bg-danger"
            if self.last_date_of_support_remaining < 365:
                return "bg-warning"
        return "bg-success"


class CiscoDeviceSupport(ChangeLoggedModel):
    objects = RestrictedQuerySet.as_manager()

    device = models.OneToOneField(to="dcim.Device", on_delete=models.CASCADE, verbose_name="Device")

    def __str__(self):
        return f"{self.device}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_cisco_support_plugin:ciscodevicesupport_list")

    def save(self, *args, **kwargs):
        # Query the Device model
        device_obj = Device.objects.select_related().get(id=self.device.id)
        # Set the name from the Device name
        self.name = device_obj.name
        # Set the pid from the Device serial
        self.serial = device_obj.serial

        # Query the DeviceType model
        device_type_obj = DeviceType.objects.select_related().get(id=self.device.device_type.id)
        # Set the pid from the DeviceType part_number
        self.pid = device_type_obj.part_number

        # Query the CiscoDeviceTypeSupport model
        cisco_device_type_support_obj = CiscoDeviceTypeSupport.objects.select_related().get(
            name=device_type_obj.model
        )
        # Set the eox_has_error from the CiscoDeviceTypeSupport eox_has_error
        self.eox_has_error = cisco_device_type_support_obj.eox_has_error
        # Set the eox_error from the CiscoDeviceTypeSupport eox_error
        self.eox_error = cisco_device_type_support_obj.eox_error
        # Set the eox_announcement_date from the CiscoDeviceTypeSupport eox_announcement_date
        self.eox_announcement_date = cisco_device_type_support_obj.eox_announcement_date
        # Set the end_of_sale_date from the CiscoDeviceTypeSupport end_of_sale_date
        self.end_of_sale_date = cisco_device_type_support_obj.end_of_sale_date
        # Set the end_of_sw_maintenance_releases from the CiscoDeviceTypeSupport end_of_sw_maintenance_releases
        self.end_of_sw_maintenance_releases = cisco_device_type_support_obj.end_of_sw_maintenance_releases
        # Set the end_of_security_vul_support_date from the CiscoDeviceTypeSupport end_of_security_vul_support_date
        self.end_of_security_vul_support_date = cisco_device_type_support_obj.end_of_security_vul_support_date
        # Set the end_of_routine_failure_analysis_date from the CiscoDeviceTypeSupport end_of_routine_failure_analysis_date
        self.end_of_routine_failure_analysis_date = (
            cisco_device_type_support_obj.end_of_routine_failure_analysis_date
        )
        # Set the end_of_service_contract_renewal from the CiscoDeviceTypeSupport end_of_service_contract_renewal
        self.end_of_service_contract_renewal = cisco_device_type_support_obj.end_of_service_contract_renewal
        # Set the end_of_svc_attach_date from the CiscoDeviceTypeSupport end_of_svc_attach_date
        self.end_of_svc_attach_date = cisco_device_type_support_obj.end_of_svc_attach_date
        # Set the last_date_of_support from the CiscoDeviceTypeSupport last_date_of_support
        self.last_date_of_support = cisco_device_type_support_obj.last_date_of_support

        # Set the api_status
        if self.sr_no_owner:
            self.api_status = "API user associated with contract and device"
        else:
            self.api_status = (
                "API user not associated with contract and device (Not authorized to most API information)"
            )

        # Set the contract_supplier
        if (
            self.contract_supplier is None
            or self.contract_supplier == "None"
            or self.contract_supplier == "Cisco SNTC"
            or self.contract_supplier == "Not covered"
            or not self.contract_supplier
        ):
            self.contract_supplier = "Cisco SNTC" if self.is_covered else "Not covered"

        # Compare the releases to set the status for desired_release to True or False
        if all(isinstance(value, str) for value in [self.desired_release, self.recommended_release]):
            self.desired_release_status = True if self.desired_release in self.recommended_release else False
        else:
            self.desired_release_status = False

        # Compare the releases to set the status for current_release to True or False
        if all(isinstance(value, str) for value in [self.current_release, self.desired_release]):
            self.current_release_status = True if self.current_release in self.desired_release else False
        else:
            self.current_release_status = False

        # Call the "real" save() method.
        super().save(*args, **kwargs)

    #### Fileds same as dcim.Device #########################################################################
    # Create these fields again because referencing them from the dcim.device model was not working

    # Field get set in custom save() function
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Name")

    # Field get set in custom save() function
    serial = models.CharField(max_length=100, blank=True, null=True, verbose_name="Serial")

    #### Fileds for CiscoDeviceSupport ######################################################################

    coverage_end_date = models.DateField(blank=True, null=True, verbose_name="Coverage End Date")

    service_contract_number = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Contract Number"
    )

    service_line_descr = models.CharField(max_length=100, blank=True, null=True, verbose_name="Service Level")

    warranty_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Warranty Type")

    warranty_end_date = models.DateField(blank=True, null=True, verbose_name="Warranty End Date")

    is_covered = models.BooleanField(default=False, verbose_name="Is Covered")

    sr_no_owner = models.BooleanField(default=False, verbose_name="Serial Owner")

    contract_supplier = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Contract Supplier"
    )

    # Field get set in custom save() function
    api_status = models.CharField(max_length=100, blank=True, null=True, verbose_name="API Status")

    recommended_release = models.TextField(
        max_length=100, blank=True, null=True, verbose_name="Recommended Release"
    )

    desired_release = models.CharField(max_length=100, blank=True, null=True, verbose_name="Desired Release")

    current_release = models.CharField(max_length=100, blank=True, null=True, verbose_name="Current Release")

    # Field get set in custom save() function
    desired_release_status = models.BooleanField(default=False, verbose_name="Desired Rel. Status")

    # Field get set in custom save() function
    current_release_status = models.BooleanField(default=False, verbose_name="Current Rel. Status")

    # Field for contracts over a Cisco partner like IBM TLS
    partner_status = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Partner Contract Status"
    )

    # Field for contracts over a Cisco partner like IBM TLS
    partner_service_level = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Partner Service Level"
    )

    # Field for contracts over a Cisco partner like IBM TLS
    partner_customer_number = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Partner Customer Number"
    )

    # Field for contracts over a Cisco partner like IBM TLS
    partner_coverage_end_date = models.DateField(
        blank=True, null=True, verbose_name="Partner Coverage End Date"
    )

    #### Property Fileds for CiscoDeviceSupport #############################################################

    # Property field for coverage end date progress bar
    @property
    def coverage_total(self):
        """
        Return 1826 days (5 years) as we cant calculate the total because we don't have the start date.
        Return None if coverage_end_date not defined.
        """
        return 1826 if self.coverage_end_date else None

    # Property field for coverage end date progress bar
    @property
    def coverage_remaining(self):
        """
        How many coverage days are remaining. Return None if coverage_end_date not defined.
        """
        if self.coverage_end_date:
            delta = self.coverage_end_date - date.today()
            return delta.days
        return None

    # Property field for coverage end date progress bar
    @property
    def coverage_elapsed(self):
        """
        How many coverage days are elaped. Return None if coverage_end_date not defined.
        """
        return self.coverage_total - self.coverage_remaining if self.coverage_end_date else None

    # Property field for coverage end date progress bar
    @property
    def coverage_progress(self):
        """
        Coverage progress in percent. Return None if coverage_end_date not defined.
        """
        return round(self.coverage_elapsed / self.coverage_total * 100) if self.coverage_end_date else None

    # Property field for coverage end date progress bar
    @property
    def coverage_progress_bar_class(self):
        """
        Coverage progress bar class.
        """
        if self.coverage_end_date:
            if self.coverage_remaining < 60:
                return "bg-danger"
            if self.coverage_remaining < 365:
                return "bg-warning"
        return "bg-success"

    # Property field for partner coverage end date progress bar
    @property
    def partner_coverage_total(self):
        """
        Return 1826 days (5 years) as we cant calculate the total because we don't have the start date.
        Return None if partner_coverage_end_date not defined.
        """
        return 1826 if self.partner_coverage_end_date else None

    # Property field for partner coverage end date progress bar
    @property
    def partner_coverage_remaining(self):
        """
        How many coverage days are remaining. Return None if partner_coverage_end_date not defined.
        """
        if self.partner_coverage_end_date:
            delta = self.partner_coverage_end_date - date.today()
            return delta.days
        return None

    # Property field for partner coverage end date progress bar
    @property
    def partner_coverage_elapsed(self):
        """
        How many coverage days are elaped. Return None if partner_coverage_end_date not defined.
        """
        return (
            self.partner_coverage_total - self.partner_coverage_remaining
            if self.partner_coverage_end_date
            else None
        )

    # Property field for partner coverage end date progress bar
    @property
    def partner_coverage_progress(self):
        """
        Coverage progress in percent. Return None if partner_coverage_end_date not defined.
        """
        return (
            round(self.partner_coverage_elapsed / self.partner_coverage_total * 100)
            if self.partner_coverage_end_date
            else None
        )

    # Property field for partner coverage end date progress bar
    @property
    def partner_coverage_progress_bar_class(self):
        """
        Coverage progress bar class.
        """
        if self.partner_coverage_end_date:
            if self.partner_coverage_remaining < 60:
                return "bg-danger"
            if self.partner_coverage_remaining < 365:
                return "bg-warning"
        return "bg-success"

    #### Fileds same as CiscoDeviceTypeSupport ##############################################################
    # Create these fields again because referencing them from the CiscoDeviceTypeSupport model was not working

    # Field get set in custom save() function
    pid = models.CharField(max_length=100, blank=True, null=True, verbose_name="PID")

    # Field get set in custom save() function
    eox_has_error = models.BooleanField(default=False, verbose_name="Has EoX Error")

    # Field get set in custom save() function
    eox_error = models.CharField(max_length=100, blank=True, null=True, verbose_name="EoX Error")

    # Field get set in custom save() function
    eox_announcement_date = models.DateField(blank=True, null=True, verbose_name="EoX Announcement Date")

    # Field get set in custom save() function
    end_of_sale_date = models.DateField(blank=True, null=True, verbose_name="End of Sale Date")

    # Field get set in custom save() function
    end_of_sw_maintenance_releases = models.DateField(
        blank=True, null=True, verbose_name="End of Sw-Maint. Date"
    )

    # Field get set in custom save() function
    end_of_security_vul_support_date = models.DateField(
        blank=True, null=True, verbose_name="End of Sec-Vul. Date"
    )

    # Field get set in custom save() function
    end_of_routine_failure_analysis_date = models.DateField(
        blank=True, null=True, verbose_name="End of Routine-Fail. Analysis Date"
    )

    # Field get set in custom save() function
    end_of_service_contract_renewal = models.DateField(
        blank=True, null=True, verbose_name="End of Service Cont. Renewal"
    )

    # Field get set in custom save() function
    end_of_svc_attach_date = models.DateField(blank=True, null=True, verbose_name="End of Svc-Attach. Date")

    # Field get set in custom save() function
    last_date_of_support = models.DateField(blank=True, null=True, verbose_name="Last Date of Support")
