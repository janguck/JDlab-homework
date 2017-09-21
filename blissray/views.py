from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "home.html"
