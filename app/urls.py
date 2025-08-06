from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("streamlit/", views.streamlit_app_view, name="streamlit_app"),
]