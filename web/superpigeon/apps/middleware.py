# Superpigeon Middleware Handler
#
# Author: Hadi Wijaya (hadi.wijaya@voidsolution.com)

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, Template, RequestContext
from datetime import date, datetime, timedelta, timezone
from django.conf import settings
from django.contrib import auth
from superpigeon.apps.api.models import TokenExpired

from rest_framework import status

import json
import requests

from superpigeon.apps.api.models import *
#import logging
#logging.basicConfig(filename='log_filename.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class DefaultMiddleware:
    """
    Provides full logging of requests and responses
    """
    _initial_http_body = None

    def __init__(self, get_response):
        self.get_response = get_response
        self._initial_http_body = None
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_request(self, request):
        self._initial_http_body = request.body

    def process_view(self, request, view_func, view_args, view_kwargs):

        if request.META.get('PATH_INFO') in settings.PROTECTED_URL:

            if request.method in ['GET', 'POST'] or request.body:
                try:
                    token = json.loads(request.body.decode("utf-8")).get('token')
                except Exception as err:
                    token = request.GET.get('token')
                request.token = token
                token_is_valid = TokenExpired.objects.filter(token__key=token, exp__gte=datetime.now(timezone.utc))
                if not token:
                    resp = {'status': 0, 'msg': 'forbidden'}
                    return HttpResponse(json.dumps(resp), content_type='application/json', status=403)
                if not token_is_valid:
                    resp = {'status':0, 'msg': 'Invalid Token or Expired'}
                    return HttpResponse(json.dumps(resp), content_type='application/json', status=403)


#    def process_response(self, request, response):
#        return response