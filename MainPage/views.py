from django.views.generic import TemplateView
from .models import ArtistProfile, Spotlight


class MainPageView(TemplateView):
    """Template view of the Main Page"""
    template_name = "MainPage/mainpage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["artist"] = ArtistProfile.objects.first()

        context["spotlights"] = Spotlight.objects.filter(
                is_public=True
                )
        return context
