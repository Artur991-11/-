from django.contrib import admin
from .models import *
# Register your models here.
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')

admin.site.register(ContactUs, ContactUsAdmin)
