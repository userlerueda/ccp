__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Ranking view...")
