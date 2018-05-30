from rest_framework import serializers
from django.contrib.auth.models import *
from rest_framework.authtoken.models import Token
from superpigeon.apps.api.models import UserProfile, Organization, Product, Dimension, Category, Tag, Image, Attribute, DefaultAttribute, MetaData

#class UserSerializer(serializers.Serializer):
#    id = serializers.IntegerField()
#    email = serializers.EmailField()
#    username = serializers.CharField(max_length=200)
#    first_name = serializers.CharField(max_length=200)
#    password = serializers.CharField(max_length=200)
#    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.filter(user=self), many=True)
#    is_superuser = serializers.BooleanField()
    #created = serializers.DateTimeField()

class GroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )

class OrganizationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class DimensionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = '__all__'

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class AttributeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

class DefaultAttributeSerializers(serializers.ModelSerializer):
    class Meta:
        model = DefaultAttribute
        fields = '__all__'

class MetaDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = MetaData
        fields = '__all__'

class UserProfileSerializers(serializers.ModelSerializer):
    organization = OrganizationSerializers()
    class Meta:
        model = UserProfile
        fields = ('id', 'phone', 'address', 'organization')

class TokenSerializers(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializers()
    groups = GroupSerializers(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'last_login', 'date_joined', 'userprofile', 'groups')

#class ModelsSerializer(serializers.ModelSerializer):
#    class Meta:
#        model 		= <models>
#        fields 		= '__all__'

