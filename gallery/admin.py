from django.contrib import admin
from .models import Album, GalleryImage


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = (
            "title",
            "album",
            "uploaded_at",
            "is_public",
            )

    list_filter = ("album", "is_public")

    search_fields = ("title", "discription")

