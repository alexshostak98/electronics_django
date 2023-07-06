from django.contrib import admin
from contacts.models import Address, Email, Contacts

admin.site.register(Address)


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'company',
        'address',
    )


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'description',
    )
