__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
