from django.contrib import admin
from .models import Tenant

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'domain', 'contact_email')
    search_fields = ('store_name', 'domain', 'contact_email')