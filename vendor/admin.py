from django.contrib import admin

# Register your models here.
from vendor.models import Vendor,VendorRequest

admin.site.register(Vendor)
@admin.register(VendorRequest)
class VendorRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['user__email']
    ordering = ['-created_at']