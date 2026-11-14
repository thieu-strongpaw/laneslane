from django.contrib import admin
from .models import ArtistProfile, Spotlight


class Spotlightinline(admin.StackedInline):
    model = Spotlight
    extra = 0


@admin.register(ArtistProfile)
class ArtistProfileAdmin(admin.ModelAdmin):
    inlines = [Spotlightinline]
    fieldsets = (("Artist introduction", {"fields": ("title", "description", "main_image"), "description": "Introduce yourself on the home page. Add featured artwork in Spotlights below."}),)

    def has_add_permission(self, request):
        return (
                super().has_add_permission(request)
                and not ArtistProfile.objects.exists()
                )

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Spotlight)
class SpotlightAdmin(admin.ModelAdmin):
    list_display = (
            "title",
            "is_public",
            "display_order",
            )

    list_filter = ("is_public",)

    list_editable = (
            "is_public",
            "display_order",
            )


admin.site.site_header = "Lane's Lane · Artist studio"
admin.site.site_title = "Lane's Lane studio"
admin.site.index_title = "Manage your artwork and website"
