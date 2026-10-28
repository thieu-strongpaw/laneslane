from django.views.generic import TemplateView


class MainPageView(TemplateView):
    """Template view of the Main Page"""
    template_name = "MainPage/mainpage.html"
