from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse
from company.models import Company
from contacts.models import Contacts
from company.messages import SUCCESS_MESSAGES


class ContactsInline(admin.TabularInline):
    model = Contacts


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'level',
        'name',
        'company_type',
        'debt_to_supplier',
        'creation_date',
        'get_supplier_url'
    )
    exclude = ('level', 'creation_date')
    list_display_links = ['name']
    list_filter = ['contacts__address__city']
    actions = ['reset_debt_to_supplier']
    ordering = ['level']
    inlines = [ContactsInline]

    def get_supplier_url(self, obj):
        supplier = obj.supplier
        if supplier:
            url = reverse(
                'admin:{}_{}_change'.format(
                    obj.get_model_app_label(),
                    obj.get_model_name(),
                ),
                args=[supplier.id],
            )
            template = '<a href={}><b>{}</b></a>'
            return format_html(template, url, supplier)

    get_supplier_url.short_description = 'Supplier'

    def reset_debt_to_supplier(self, request, queryset):
        queryset.filter(supplier__isnull=False).update(debt_to_supplier=0)
        self.message_user(
            request,
            message=SUCCESS_MESSAGES['reset_debt'],
            level=messages.SUCCESS,
        )
