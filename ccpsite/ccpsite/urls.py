"""ccpsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/ranking/", include("ranking.urls")),
    path("api/universaltennis/", include("universaltennis.urls")),
    path("universaltennis/", include("universaltennis.urls")),
    path("api/tournamentsw/", include("tournamentsw.urls")),
    path("api/results/", include("results.urls")),
    path("admin/", admin.site.urls),
]
