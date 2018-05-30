from django.contrib import admin
from superpigeon.apps.api.models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.fields if field.name != "id"]

class OrganizationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Organization._meta.fields if field.name != "id"]

class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields if field.name != "id"]

class DownloadAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Download._meta.fields if field.name != "id"]

class DimensionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Dimension._meta.fields if field.name != "id"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields if field.name != "id"]

class TagAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tag._meta.fields if field.name != "id"]

class ImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Image._meta.fields if field.name != "id"]

class AttributeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Attribute._meta.fields if field.name != "id"]

class DefaultAttributeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DefaultAttribute._meta.fields if field.name != "id"]

class MetaDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MetaData._meta.fields if field.name != "id"]

class BillingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Billing._meta.fields if field.name != "id"]

class CouponLineAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CouponLine._meta.fields if field.name != "id"]

class CustomerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Customer._meta.fields if field.name != "id"]

class FeeLineAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FeeLine._meta.fields if field.name != "id"]

class LineItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LineItem._meta.fields if field.name != "id"]

class LinkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Link._meta.fields if field.name != "id"]

class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields if field.name != "id"]

class RefundAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Refund._meta.fields if field.name != "id"]

class ShippingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Shipping._meta.fields if field.name != "id"]

class ShippingLineAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ShippingLine._meta.fields if field.name != "id"]

class TaxLineAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TaxLine._meta.fields if field.name != "id"]


# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Download, DownloadAdmin)
admin.site.register(Dimension, DimensionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(DefaultAttribute, DefaultAttributeAdmin)
admin.site.register(MetaData, MetaDataAdmin)

admin.site.register(Billing, BillingAdmin)
admin.site.register(CouponLine, CouponLineAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(FeeLine, FeeLineAdmin)
admin.site.register(LineItem, LineItemAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Refund, RefundAdmin)
admin.site.register(Shipping, ShippingAdmin)
admin.site.register(ShippingLine, ShippingLineAdmin)
admin.site.register(TaxLine, TaxLineAdmin)

admin.site.register(TokenExpired)
admin.site.register(Organization, OrganizationAdmin)