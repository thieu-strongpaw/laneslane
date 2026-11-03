from django.contrib import admin
from .models import ArtistProfile, Spotlight


class Spotlightinline(admin.StackedInline):
    model = Spotlight
    extra = 0


@admin.register(ArtistProfile)
class ArtistProfileAdmin(admin.ModelAdmin):
    inlines = [Spotlightinline]

    def has_add_permission(sefl, request):
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

