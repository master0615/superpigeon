from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import datetime, timezone
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

class UserProfile(models.Model):
    history = AuditlogHistoryField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    photo = models.ImageField(upload_to='photo', null=True, blank=True)

    def __str__(self):
        return '%s' % self.user

class TokenExpired(models.Model):
    history = AuditlogHistoryField()
    token = models.OneToOneField(Token, on_delete=models.CASCADE)
    exp = models.DateTimeField(null=True, blank=True)

    def has_expired(self):
        if self.exp < datetime.now(timezone.utc):
            return True
        return False

    def __str__(self):
        return '%s' % self.token

class Organization(models.Model):
    history = AuditlogHistoryField()
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    admins = models.ManyToManyField(UserProfile, related_name='admin_user', blank=True)

    def __str__(self):
        return '%s' % self.business_name

class Link(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    href = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.href

class Billing(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    address_1 = models.TextField(null=True, blank=True)
    address_2 = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    postcode = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return '%s' % self.first_name

class Shipping(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    address_1 = models.TextField(null=True, blank=True)
    address_2 = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    postcode = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return '%s' % self.first_name


class Customer(models.Model):
    date_created = models.DateTimeField(null=True, blank=True)
    date_created_gmt = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    date_modified_gmt = models.DateTimeField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    billing = models.ForeignKey('Billing', null=True, blank=True, on_delete=models.CASCADE)
    shipping = models.ForeignKey('Shipping', null=True, blank=True, on_delete=models.CASCADE)
    is_paying_customer = models.BooleanField(default=False)
    orders_count = models.IntegerField(default=0)
    total_spent = models.FloatField(default=0.00)
    avatar_url = models.CharField(max_length=255, null=True, blank=True)
    meta_data = models.ManyToManyField('MetaData', blank=True)
    links = models.ManyToManyField('Link', blank=True)

    def __str__(self):
        return '%s' % self.username

class TaxLine(models.Model):
    rate_code = models.CharField(max_length=255, null=True, blank=True)
    rate_id = models.CharField(max_length=100, null=True, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    compound = models.BooleanField(default=False)
    tax_total = models.FloatField(default=0.00)
    shipping_tax_total = models.FloatField(default=0.00)
    meta_data = models.ManyToManyField('MetaData', blank=True)

    def __str__(self):
        return '%s' % self.rate_code

class LineItem(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    product_id = models.ForeignKey('Product', null=True, blank=True, on_delete=models.CASCADE)
    variation_id = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    tax_class = models.CharField(max_length=100, null=True, blank=True)
    subtotal = models.FloatField(default=0.00)
    subtotal_tax = models.FloatField(default=0.00)
    total = models.FloatField(default=0.00)
    total_tax = models.FloatField(default=0.00)
    taxes = models.ManyToManyField('TaxLine', blank=True)
    meta_data = models.ManyToManyField('MetaData', blank=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField(default=0.00)

    def __str__(self):
        return '%s' % self.name

class ShippingLine(models.Model):
    method_title = models.CharField(max_length=255, null=True, blank=True)
    method_id = models.CharField(max_length=100, null=True, blank=True)
    total = models.FloatField(default=0.00)
    total_tax = models.FloatField(default=0.00)
    taxes = models.ManyToManyField('TaxLine', blank=True)
    meta_data = models.ManyToManyField('MetaData', blank=True)

    def __str__(self):
        return '%s' % self.method_title

class FeeLine(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    tax_class = models.CharField(max_length=100, null=True, blank=True)
    tax_status = models.CharField(max_length=100, null=True, blank=True)
    total = models.FloatField(default=0.00)
    total_tax = models.FloatField(default=0.00)
    taxes = models.ManyToManyField('TaxLine', blank=True)
    meta_data = models.ManyToManyField('MetaData', blank=True)

    def __str__(self):
        return '%s' % self.name

class CouponLine(models.Model):
    code = models.CharField(max_length=100, null=True, blank=True)
    discount = models.FloatField(default=0.00)
    discount_tax = models.FloatField(default=0.00)
    meta_data = models.ManyToManyField('MetaData', blank=True)

    def __str__(self):
        return '%s' % self.code

class Refund(models.Model):
    reason = models.TextField(null=True, blank=True)
    total = models.FloatField(default=0.0)
    
    def __str__(self):
        return '%s' % self.total


class Order(models.Model):
    parent_id = models.ForeignKey('Order', null=True, blank=True, on_delete=models.CASCADE)
    number = models.IntegerField(null=True, blank=True)
    order_key = models.CharField(max_length=100, null=True, blank=True)
    created_via = models.CharField(max_length=100, null=True, blank=True)
    version = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    currency = models.CharField(max_length=3, null=True, blank=True)
    date_created = models.DateTimeField(null=True, blank=True)
    date_created_gmt = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    date_modified_gmt = models.DateTimeField(null=True, blank=True)
    discount_total = models.FloatField(default=0.00)
    discount_tax = models.FloatField(default=0.00)
    shipping_total = models.FloatField(default=0.00)
    shipping_tax = models.FloatField(default=0.00)
    cart_tax = models.FloatField(default=0.00)
    total = models.FloatField(default=0.00)
    total_tax = models.FloatField(default=0.00)
    prices_include_tax = models.BooleanField(default=False)
    customer_id = models.ForeignKey('Customer', null=True, blank=True, on_delete=models.CASCADE)
    customer_ip_address = models.CharField(max_length=100, null=True, blank=True)
    customer_user_agent = models.TextField(null=True, blank=True)
    customer_note = models.TextField(null=True, blank=True)
    billing = models.ForeignKey('Billing', null=True, blank=True, on_delete=models.CASCADE)
    shipping = models.ForeignKey('Shipping', null=True, blank=True, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=255, null=True, blank=True)
    payment_method_title = models.CharField(max_length=255, null=True, blank=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    date_paid = models.DateTimeField(null=True, blank=True)
    date_paid_gmt = models.DateTimeField(null=True, blank=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    date_completed_gmt = models.DateTimeField(null=True, blank=True)
    cart_hash = models.CharField(max_length=255, null=True, blank=True)
    meta_data = models.ManyToManyField('MetaData', blank=True)
    line_items = models.ManyToManyField('LineItem', blank=True)
    tax_lines = models.ManyToManyField('TaxLine', blank=True)
    shipping_lines = models.ManyToManyField('ShippingLine', blank=True)
    fee_lines = models.ManyToManyField('FeeLine', blank=True)
    coupon_lines = models.ManyToManyField('CouponLine', blank=True)
    refunds = models.ManyToManyField('Refund', blank=True)
    links = models.ManyToManyField('Link', blank=True)


class Product(models.Model):
    TYPES = (
        ('simple', 'Simple'),
        ('grouped', 'Grouped'),
        ('external', 'External'),
        ('variable', 'Variable')
    )

    STATUS = (
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('private', 'Private'),
        ('publish', 'Publish')
    )

    TAX_STATUS = (
        ('taxable', 'Taxable'),
        ('shipping', 'Shipping')
    )

    BACKORDERS = (
        ('no', 'No'),
        ('notify', 'Notify'),
        ('yes', 'Yes')
    )

    history = AuditlogHistoryField()
    external_string_id = models.CharField(max_length=255, null=True, blank=True)
    external_int_id = models.IntegerField(null=True, blank=True)
    external_source_type = models.CharField(max_length=255, null=True, blank=True)
    external_source_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    permalink = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(null=True, blank=True)
    date_created_gmt = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    date_modified_gmt = models.DateTimeField(null=True, blank=True)
    types = models.CharField(max_length=20, choices=TYPES, default='simple')
    status = models.CharField(max_length=20, choices=STATUS, default='publish')
    description = models.TextField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    sku = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    regular_price = models.FloatField(null=True, blank=True)
    sale_price = models.FloatField(null=True, blank=True)
    date_on_sale_from = models.DateTimeField(null=True, blank=True)
    date_on_sale_from_gmt = models.DateTimeField(null=True, blank=True)
    date_on_sale_to = models.DateTimeField(null=True, blank=True)
    date_on_sale_to_gmt = models.DateTimeField(null=True, blank=True)
    price_html = models.TextField(null=True, blank=True)
    on_sale = models.NullBooleanField(blank=True)
    purchasable = models.NullBooleanField(blank=True)
    total_sales = models.IntegerField(null=True, blank=True)
    virtual = models.BooleanField(default=False)
    downloadable = models.BooleanField(default=False)
    downloads = models.ManyToManyField('Download', blank=True)
    download_limit = models.IntegerField(default=-1)
    download_expiry = models.IntegerField(default=-1)
    tax_status = models.CharField(max_length=20, choices=TAX_STATUS, null=True, blank=True, default='taxable')
    tax_class = models.CharField(max_length=255, null=True, blank=True)
    manage_stock = models.BooleanField(default=False)
    stock_quantity = models.IntegerField(null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    backorders = models.CharField(max_length=20, choices=BACKORDERS, default='no')
    backorders_allowed = models.NullBooleanField(blank=True)
    backordered = models.NullBooleanField(blank=True)
    sold_individually = models.BooleanField(default=False)
    weight = models.FloatField(null=True, blank=True)
    dimensions = models.ForeignKey('Dimension', null=True, blank=True, on_delete=models.CASCADE)
    shipping_required = models.NullBooleanField(blank=True)
    shipping_taxable = models.NullBooleanField(blank=True)
    shipping_class = models.CharField(max_length=255, null=True, blank=True)
    shipping_class_id = models.IntegerField(null=True, blank=True)
    reviews_allowed = models.BooleanField(default=False)
    average_rating = models.FloatField(null=True, blank=True)
    rating_count = models.IntegerField(null=True, blank=True)
    related_ids = models.ManyToManyField('Product', related_name='related_product', blank=True)
    upsell_ids = models.ManyToManyField('Product', related_name='upsell_product', blank=True)
    cross_sell_ids = models.ManyToManyField('Product', related_name='cross_sell_product', blank=True)
    parent_id = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True)
    purchase_note = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField('Category', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    images = models.ManyToManyField('Image', blank=True)
    attributes = models.ManyToManyField('Attribute', blank=True)
    default_attributes = models.ManyToManyField('DefaultAttribute', blank=True)
    variations = models.ManyToManyField('Product', related_name='variations_product', blank=True)
    grouped_products = models.ManyToManyField('Product', related_name='grouped_product', blank=True)
    menu_order = models.IntegerField(null=True, blank=True)
    meta_data = models.ManyToManyField('MetaData', blank=True)

    def __str__(self):
        return '%s' % self.id


class Download(models.Model):
    name = models.CharField(max_length=255)
    file = models.TextField()

    def __str__(self):
        return '%s' % self.id

class Dimension(models.Model):
    length = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.id

class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '%s' % self.id

class Tag(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '%s' % self.id

class Image(models.Model):
    date_created = models.DateTimeField(null=True, blank=True)
    date_created_gmt = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    date_modified_gmt = models.DateTimeField(null=True, blank=True)
    src = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    alt = models.CharField(max_length=255, null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.id

class Attribute(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    visible = models.BooleanField(default=False)
    variation = models.BooleanField(default=False)
    options = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.id

class DefaultAttribute(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    option = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.id


class MetaData(models.Model):
    key = models.CharField(max_length=255, null=True, blank=True)
    value = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.key


auditlog.register(User)
auditlog.register(UserProfile)
auditlog.register(TokenExpired)
auditlog.register(Organization)
auditlog.register(Product)