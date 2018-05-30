from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django import forms
from .models import *

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.forms.models import model_to_dict
from datetime import datetime, timedelta, timezone


from superpigeon.apps.api.models import *
from superpigeon.apps.api.serializer import *
from superpigeon.tasks import *

import logging
db_logger = logging.getLogger('superpigeon api')


class ProfileViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    def list(self, request):
        api_result = UserSerializer(User.objects.all(), many=True)
        return Response(api_result.data, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            token = Token.objects.get(key=request.token)
            up = UserProfile.objects.get(user=token.user)
            if request.data.get('phone'):
                up.phone = request.data.get('phone')
            if request.data.get('address'):
                up.address = request.data.get('address')
            up.save()

            try:
                o = Organization.objects.get(user=up)
            except Exception as err:
                pass
            else:
                if request.data.get('business_name'):
                    o.business_name = request.data.get('business_name')
                if request.data.get('business_address'):
                    o.address = request.data.get('business_address')
                if request.data.get('business_phone'):
                    o.phone = request.data.get('business_phone')
                if request.data.get('admins'):
                    for i in request.data.get('admins'):
                        o.admins.add(UserProfile.objects.get(user__id=i))
                if request.data.get('remove_admins'):
                    for i in request.data.get('remove_admins'):
                        o.admins.remove(UserProfile.objects.get(user__id=i))
                o.save()
        except Exception as err:
            data = {'status':0, 'msg':str(err)}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            data = {'status':1, 'msg':'success'}
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response()


    def partial_update(self, request, email=None):
        return Response()

    def destroy(self, request, email=None):
        return Response()

class SignupViewSet(viewsets.ViewSet):

    """
<div>Example json for full signup as organization:</div>
<pre>{
"username": "tester",
"password": "testertester",
"email":"test5@test.com",
"first_name":"hallo",
"last_name":"hello",
"address":"test test test",
"phone":"1982319203",
"business_name":"voidsolution",
"business_phone":"122222222",
"business_address":"address business"
}
</pre>

<div>Example json signup without organization:</div>
<pre>
{
"username": "tester",
"password": "testertester",
"email":"test5@test.com",
"first_name":"hallo",
"last_name":"hello",
"address":"test test test",
"phone":"1982319203"
}
</pre>
"""

    queryset = User.objects.all()
    def create(self, request):
        try:
            forms.EmailField(error_messages={'required': 'Email required'}).clean(request.data.get('email'))
            forms.CharField(error_messages={'required': 'Password required'}).clean(request.data.get('password'))
            user = User.objects.create_user(
                username=request.data.get('email'),
                email=request.data.get('email'),
                password=request.data.get('password'),
            )
            if request.data.get('first_name'):
                user.first_name = request.data.get('first_name')
            if request.data.get('last_name'):
                user.last_name = request.data.get('last_name')
            user.save()
            user_profile = UserProfile.objects.create(user=User.objects.get(id=user.id), phone=request.data.get('phone'), address=request.data.get('address'))

            if request.data.get('business_name'):
                Organization.objects.create(user=UserProfile.objects.get(id=user_profile.id), business_name=request.data.get('business_name'), phone=request.data.get('business_phone'), address=request.data.get('business_address'))

        except Exception as err:
            data = {'status': 0, 'msg': str(err)}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthViewSet(viewsets.ViewSet):
    # Router class variables
    #lookup_field = 'email'
    #lookup_value_regex = '[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}'

    # Viewsets class variables
    #queryset = User.objects.all()

    """
    <div>Get new token with expire time (in hours)</div>
    <div>example json for get token with 1 hour expire:</div>
    <pre>{"email": "tester@mail.com", "password": "tester", "exp_hour":1}</pre>
    <div>example json for get token with 4 hour expire (default):</div>
    <pre>{"email": "tester@mail.com", "password": "tester"}</pre>
    """

    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        data = {'status': 1, 'msg': 'empty'}
        db_logger.info(request.data)
        if email and password:
            try:
                u = User.objects.get(email=email)
                if u.check_password(password):
                    try:
                        token = Token.objects.get(user=u)
                        if TokenExpired.objects.get(token=token).has_expired():
                            token.delete()
                            raise Exception
                    except Exception:
                        token = Token.objects.create(user=u)
                    try:
                        te = TokenExpired.objects.get(token=token)
                        if TokenExpired.objects.get(token=token).has_expired():
                            te.delete()
                            raise Exception
                    except Exception:
                        delta = timedelta(hours=4)
                        if request.data.get('exp_hour'):
                            delta = timedelta(hours=request.data.get('exp_hour', 4))
                        if request.data.get('exp_min'):
                            delta = timedelta(minutes=request.data.get('exp_min', 1))
                        if request.data.get('exp_sec'):
                            delta = timedelta(seconds=request.data.get('exp_sec', 60))
                        exp = datetime.now(timezone.utc) + delta
                        te = TokenExpired.objects.create(token=token, exp=exp)
                    s = UserSerializer(u).data
                    delta_exp = te.exp - datetime.now(timezone.utc)
                    s.update({'token': token.key, 'exp':delta_exp.seconds, 'status':1, 'msg':'success'})
                    data = s

                    db_logger.info(data)
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    raise Exception('Incorrect password')
            except Exception as err:
                db_logger.exception(err)
                data = {'status':0 ,'msg': str(err)}
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data, status=status.HTTP_404_NOT_FOUND)

class LogoutViewSet(viewsets.ViewSet):

    """
    <div>Destroy token</div>
    <div>example json for destroy token</div>
    <pre>{"token":"b4ccfed856b984ded6b5e9be95c0fedc812b00be"}</pre>
    """

    def create(self, request):
        token = request.data.get('token')
        data = {'please move along': 'nothing to see here'}
        if token:
            try:
                Token.objects.get(key=token).delete()
            except Exception as err:
                data = {'error': str(err)}
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                data = {'success': token}
            return Response(data, status=status.HTTP_200_OK)
        return Response(data, status=status.HTTP_404_NOT_FOUND)

class SyncProductViewSet(viewsets.ViewSet):

    """
    <div>Sync product with woocommerce</div>
    """
    def list(self, request):
        data = {'please move along': 'nothing to see here'}
        try:
            woocommerce_get_product()
        except Exception as err:
            data = {'error': str(err)}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            data = {'success': 'proceed on background'}

        return Response(data, status=status.HTTP_200_OK)

class SyncOrderViewSet(viewsets.ViewSet):

    """
    <div>Sync order with woocommerce</div>
    """
    def list(self, request):
        data = {'please move along': 'nothing to see here'}
        try:
            woocommerce_get_order()
        except Exception as err:
            data = {'error': str(err)}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            data = {'success': 'proceed on background'}

        return Response(data, status=status.HTTP_200_OK)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

class DimensionViewSet(viewsets.ModelViewSet):
    queryset = Dimension.objects.all()
    serializer_class = DimensionSerializers

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializers

class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializers

class DefaultAttributeViewSet(viewsets.ModelViewSet):
    queryset = DefaultAttribute.objects.all()
    serializer_class = DefaultAttributeSerializers

class MetaDataViewSet(viewsets.ModelViewSet):
    queryset = MetaData.objects.all()
    serializer_class = MetaDataSerializers
