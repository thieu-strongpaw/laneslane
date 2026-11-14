from django.contrib import admin
from .models import ContactInfo

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Page introduction", {"fields": ("heading", "introduction")}),
        ("Public contact details", {"fields": ("email", "phone", "studio_details"), "description": "Everything entered here appears on your public contact page. Leave unused fields blank."}),
        ("Social profile or shop", {"fields": ("website_label", "website_url")}),
    )

    def has_add_permission(self, request):
        return super().has_add_permission(request) and not ContactInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
