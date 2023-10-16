from collections import defaultdict
from django.utils.translation import gettext_lazy
from netbox.views import generic
from . import filtersets, models, tables, forms


#### Cisco Device Support ###################################################################################


class CiscoDeviceSupportListView(generic.ObjectListView):
    queryset = models.CiscoDeviceSupport.objects.all()
    filterset = filtersets.CiscoDeviceSupportFilterSet
    filterset_form = forms.CiscoDeviceSupportFilterForm
    table = tables.CiscoDeviceSupportTable
    actions = ("export", "delete")


class CiscoDeviceSupportDeleteView(generic.ObjectDeleteView):
    queryset = models.CiscoDeviceSupport.objects.all()


class CiscoDeviceSupportBulkDeleteView(generic.BulkDeleteView):
    queryset = models.CiscoDeviceSupport.objects.all()
    filterset = filtersets.CiscoDeviceSupportFilterSet
    table = tables.CiscoDeviceSupport


#### Cisco Device Type Support ##############################################################################


class CiscoDeviceTypeSupportListView(generic.ObjectListView):
    queryset = models.CiscoDeviceTypeSupport.objects.all()
    filterset = filtersets.CiscoDeviceTypeSupportFilterSet
    filterset_form = forms.CiscoDeviceTypeSupportFilterForm
    table = tables.CiscoDeviceTypeSupportTable
    actions = ("export", "delete")


class CiscoDeviceTypeSupportDeleteView(generic.ObjectDeleteView):
    queryset = models.CiscoDeviceTypeSupport.objects.all()


class CiscoDeviceTypeSupportBulkDeleteView(generic.BulkDeleteView):
    queryset = models.CiscoDeviceTypeSupport.objects.all()
    filterset = filtersets.CiscoDeviceTypeSupportFilterSet
    table = tables.CiscoDeviceTypeSupport
