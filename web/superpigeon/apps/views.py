from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from redis import Redis
import os

redis = Redis(host='redis', port=os.environ.get('REDIS_PORT', 6379))


def home(request):
    return HttpResponse('Hello SuperPigeon')