from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from redis import Redis


redis = Redis(host='redis', port=6379)


def home(request):
    return HttpResponse('Hello SuperPigeon 2')