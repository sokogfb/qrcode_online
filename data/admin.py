from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from data.models import Employee


class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        # skip_unchanged = True
        # report_skipped = False
        fields = (
            'id', 'title', 'family_name', 'given_name', 'org', 'adr', 'email', 'work_phone', 'mobile_phone', 'fax',
            'direct_line',
            'website')
        export_order = (
            'id', 'title', 'family_name', 'given_name', 'org', 'adr', 'email', 'work_phone', 'mobile_phone', 'fax',
            'direct_line',
            'website')


class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    list_filter = (
        'id', 'title', 'family_name', 'given_name', 'org', 'adr', 'email', 'work_phone', 'mobile_phone', 'fax',
        'direct_line',
        'website')
    list_display = (
        'id', 'title', 'family_name', 'given_name', 'org', 'adr', 'email', 'work_phone', 'mobile_phone', 'fax',
        'direct_line',
        'website')
    search_fields = ('family_name', 'given_name', 'email', 'work_phone', 'mobile_phone', 'direct_line')
    list_per_page = 20


admin.site.register(Employee, EmployeeAdmin)
