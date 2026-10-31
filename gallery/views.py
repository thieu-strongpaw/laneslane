from django.views.generic import ListView
from .models import GalleryImage

class GalleryView(ListView):
    """Template view of the Gallery Page"""
    model =  GalleryImage
    template_name = "gallery/gallery.html"
    context_object_name = "images"


