from django.contrib import admin
from contacts.models import Address, Email, Contacts

admin.site.register(Address)
admin.site.register(Email)
admin.site.register(Contacts)
