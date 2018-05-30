#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import re

import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superpigeon.settings")

from celery import task

from woocommerce import API
from datetime import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail, EmailMessage

import json
import time
import pytz

wcapi = API(
    url=settings.WOOCOMMERCE_URL,
    consumer_key=settings.WOOCOMMERCE_CONSUMER_KEY,
    consumer_secret=settings.WOOCOMMERCE_CONSUMER_SECRET,
    wp_api=True,
    version="wc/v2",
    query_string_auth=True
)


@task()
def email_send(subject, to, msg, fr=None, title=''):
    print('subject: %s' % subject)
    print('to: %s' % to)
    headers = {'Reply-To': fr}

    while True:
        try:
            subject = subject
            html_content = msg
            to = [to]
            e = EmailMessage(subject, html_content, '%s <%s>' % (title, fr), to, headers=headers)
#            if attachment_id:
#                for i in json.loads(attachment_id):
#                    f = Attachment.objects.get(id=i)
#                    e.attach(f.file.name, f.file.read())
            e.content_subtype = "html"
            e.send(fail_silently=False)
        except Exception as err:
            print(err)
            break
        else:
            print('Email Status: Success to: %s' % to)
            break
    return True


@task()
def woocommerce_get_product():
    from superpigeon.apps.api.models import Product, MetaData, Download, Tag, Category, Attribute, DefaultAttribute, Image
    try:
        data = wcapi.get("products").json()
        for i in data:
            try:
                p = Product.objects.get(id=i['id'])
            except Exception:
                p = Product()

            p.id = i['id']
            p.name = i['name']
            p.slug = i['slug']

            if i.get('weight'):
                p.weight = i.get('weight')

            p.permalink = i['permalink']
            if i.get('sale_price'):
                p.sale_price = i.get('sale_price')
            p.sold_individually = i['sold_individually']
            p.download_limit = i['download_limit']

            if i.get('date_created_gmt'):
                p.date_created_gmt = pytz.utc.localize(datetime.strptime(i.get('date_created_gmt'), '%Y-%m-%dT%H:%M:%S'))

            p.reviews_allowed = i['reviews_allowed']
            p.shipping_required = i['shipping_required']
            p.button_text = i['button_text']

            if i.get('date_on_sale_to_gmt'):
                p.date_on_sale_to_gmt = pytz.utc.localize(datetime.strptime(i.get('date_on_sale_to_gmt'), '%Y-%m-%dT%H:%M:%S'))

            p.tax_class = i['tax_class']
            p.menu_order = i['menu_order']
            p.on_sale = i['on_sale']
            p.purchase_note = i['purchase_note']

            if i.get('date_on_sale_to'):
                p.date_on_sale_to = pytz.utc.localize(datetime.strptime(i.get('date_on_sale_to'), '%Y-%m-%dT%H:%M:%S'))

            p.backordered = i['backordered']
            p.catalog_visibility = i['catalog_visibility']
            p.rating_count = i['rating_count']
            p.tax_status = i['tax_status']

            if i.get('date_modified'):
                p.date_modified = pytz.utc.localize(datetime.strptime(i.get('date_modified'), '%Y-%m-%dT%H:%M:%S'))

            p.price_html = i['price_html']

            if i.get('date_on_sale_from_gmt'):
                p.date_on_sale_from_gmt = pytz.utc.localize(datetime.strptime(i.get('date_on_sale_from_gmt'), '%Y-%m-%dT%H:%M:%S'))

            p.total_sales = i['total_sales']
            p.description = i['description']
            p.in_stock = i['in_stock']

            if i.get('price'):
                p.price = i.get('price')
            p.purchasable = i['purchasable']

            if i.get('date_modified_gmt'):
                p.date_modified_gmt = pytz.utc.localize(datetime.strptime(i.get('date_modified_gmt'), '%Y-%m-%dT%H:%M:%S'))

            if i.get('regular_price'):
                p.regular_price = i.get('regular_price')
            p.virtual = i['virtual']
            p.shipping_taxable = i['shipping_taxable']

            if i.get('date_created'):
                p.date_created = pytz.utc.localize(datetime.strptime(i.get('date_created'), '%Y-%m-%dT%H:%M:%S'))

            p.shipping_class = i['shipping_class']

            if i.get('average_rating'):
                p.average_rating = i.get('average_rating')

            if i.get('parent_id'):
                try:
                    pid = Product.objects.get(id=i.get('parent_id'))
                except Exception:
                    pass
                else:
                    p.parent_id = pid

            p.backorders = i['backorders']
            p.backorders_allowed = i['backorders_allowed']
            p.stock_quantity = i['stock_quantity']
            p.status = i['status']
            p.download_expiry = i['download_expiry']
            p.featured = i['featured']
            p.downloadable = i['downloadable']

            if i.get('date_on_sale_from'):
                p.date_on_sale_from = pytz.utc.localize(datetime.strptime(i.get('date_on_sale_from'), '%Y-%m-%dT%H:%M:%S'))


            p.sku = i['sku']
            p.manage_stock = i['manage_stock']
            p.type = i['type']
            p.short_description = i['short_description']
            p.external_url = i['external_url']
            p.save()
            if i.get('meta_data'):
                for x in i.get('meta_data'):
                    try:
                        m = MetaData.objects.get(key=x.get('key'))
                    except Exception:
                        m = MetaData()
                    m.key = x.get('key')
                    m.value = json.dumps(x.get('value'))
                    m.save()
                    p.meta_data.add(m)

            if i.get('cross_sell_ids'):
                for x in i.get('cross_sell_ids'):
                    try:
                        pr = Product.objects.get(id=x['id'])
                    except Exception:
                        pass
                    else:
                        p.cross_sell_ids.add(pr)

            if i.get('downloads'):
                for x in i.get('downloads'):
                    try:
                        d = Download.objects.get(id=x['id'])
                    except Exception:
                        d = Download()
                    d.id = x['id']
                    d.name = x['name']
                    d.file = x['file']
                    d.save()
                    p.downloads.add(d)

            if i.get('tags'):
                for x in i.get('tags'):
                    try:
                        t = Tag.objects.get(id=x['id'])
                    except Exception:
                        t = Tag()
                    t.id = x['id']
                    t.name = x['name']
                    t.slug = x['slug']
                    t.save()
                    p.tags.add(t)

            if i.get('default_attributes'):
                for x in i.get('default_attributes'):
                    try:
                        da = DefaultAttribute.objects.get(id=x['id'])
                    except Exception:
                        da = DefaultAttribute()
                    da.id = x['id']
                    da.name = x['name']
                    da.option = json.dumps(x['option'])
                    da.save()
                    p.tags.add(da)

            if i.get('grouped_products'):
                for x in i.get('grouped_products'):
                    try:
                        pr = Product.objects.get(id=x['id'])
                    except Exception:
                        pass
                    else:
                        p.grouped_products.add(pr)

            if i.get('related_ids'):
                for x in i.get('related_ids'):
                    try:
                        pr = Product.objects.get(id=x['id'])
                    except Exception:
                        pass
                    else:
                        p.related_ids.add(pr)

            if i.get('variations'):
                for x in i.get('variations'):
                    try:
                        pr = Product.objects.get(id=x['id'])
                    except Exception:
                        pass
                    else:
                        p.variations.add(pr)

            if i.get('upsell_ids'):
                for x in i.get('upsell_ids'):
                    try:
                        pr = Product.objects.get(id=x['id'])
                    except Exception:
                        pass
                    else:
                        p.upsell_ids.add(pr)

            if i.get('images'):
                for x in i.get('images'):
                    try:
                        im = Image.objects.get(id=x['id'])
                    except Exception:
                        im = Image()
                    im.id = x['id']

                    if x.get('date_created'):
                        im.date_created = pytz.utc.localize(datetime.strptime(x.get('date_created'), '%Y-%m-%dT%H:%M:%S'))

                    if x.get('date_created_gmt'):
                        im.date_created_gmt = pytz.utc.localize(datetime.strptime(x.get('date_created_gmt'), '%Y-%m-%dT%H:%M:%S'))

                    if x.get('date_modified'):
                        im.date_modified = pytz.utc.localize(datetime.strptime(x.get('date_modified'), '%Y-%m-%dT%H:%M:%S'))


                    if x.get('date_modified_gmt'):
                        im.date_modified_gmt = pytz.utc.localize(datetime.strptime(x.get('date_modified_gmt'), '%Y-%m-%dT%H:%M:%S'))

                    im.src = x['src']
                    im.name = x['name']
                    im.alt = x['alt']
                    im.position = x['position']
                    im.save()
                    p.images.add(im)

            if i.get('attributes'):
                for x in i.get('attributes'):
                    try:
                        a = Attribute.objects.get(id=x['id'])
                    except Exception:
                        a = Attribute()
                    a.id = x['id']
                    a.name = x['name']
                    a.position = x['position']
                    a.visible = x['visible']
                    a.variation = x['variation']
                    a.options = json.dumps(x['option'])
                    a.save()

                    p.attributes.add(a)

            if i.get('categories'):
                for x in i.get('categories'):
                    try:
                        c = Category.objects.get(id=x['id'])
                    except Exception:
                        c = Category()
                    c.id = x['id']
                    c.name = x['name']
                    c.slug = x['slug']
                    c.save()

                    p.categories.add(c)

            p.save()
    except Exception as err:
        return {'result': str(err)}
    return {'result': data}




@task()
def woocommerce_get_order():
    from superpigeon.apps.api.models import Product, Order, Customer, Billing, Shipping, MetaData, LineItem, TaxLine, ShippingLine, FeeLine, CouponLine, Refund
    try:
        data = wcapi.get("orders").json()
        for i in data:
            try:
                o = Order.objects.get(id=i['id'])
            except Exception:
                o = Order()
            o.id = i['id']
            if i.get('parent_id'):
                try:
                    oid = Order.objects.get(id=i.get('parent_id'))
                    o.parent_id = oid
                except Exception:
                    pass
            o.number = i['number']
            o.order_key = i['order_key']
            o.created_via = i['created_via']
            o.version = i['version']
            o.status = i['status']
            o.currency = i['currency']
            if i.get('date_created'):
                o.date_created = pytz.utc.localize(datetime.strptime(i.get('date_created'), '%Y-%m-%dT%H:%M:%S'))
            if i.get('date_created_gmt'):
                o.date_created_gmt = pytz.utc.localize(datetime.strptime(i.get('date_created_gmt'), '%Y-%m-%dT%H:%M:%S'))
            if i.get('date_modified'):
                o.date_modified = pytz.utc.localize(datetime.strptime(i.get('date_modified'), '%Y-%m-%dT%H:%M:%S'))
            if i.get('date_modified_gmt'):
                o.date_modified_gmt = pytz.utc.localize(datetime.strptime(i.get('date_modified_gmt'), '%Y-%m-%dT%H:%M:%S'))
            o.discount_total = i.get('discount_total', 0.00)
            o.discount_tax = i.get('discount_tax', 0.00)
            o.shipping_total = i.get('shipping_total', 0.00)
            o.shipping_tax = i.get('shipping_tax', 0.00)
            o.cart_tax = i.get('cart_tax', 0.00)
            o.total = i.get('total', 0.00)
            o.total_tax = i.get('total_tax', 0.00)
            o.prices_include_tax = i.get('prices_include_tax', False)
            if i.get('customer_id'):
                try:
                    o.customer_id = Customer.objects.get(id=i.get('customer_id'))
                except Exception:
                    pass
            o.customer_ip_address = i.get('customer_ip_address')
            o.customer_user_agent = i.get('customer_user_agent')
            o.customer_note = i.get('customer_note')
            if i.get('billing'):
                try:
                    b = Billing.objects.get(email=i.get('billing').get('email'))
                except Exception:
                    b = Billing()
                b.id = i.get('billing').get('id')
                b.first_name = i.get('billing').get('first_name')
                b.last_name = i.get('billing').get('last_name')
                b.company = i.get('billing').get('company')
                b.address_1 = i.get('billing').get('address_1')
                b.address_2 = i.get('billing').get('address_2')
                b.city = i.get('billing').get('city')
                b.state = i.get('billing').get('state')
                b.postcode = i.get('billing').get('postcode')
                b.country = i.get('billing').get('country')
                b.email = i.get('billing').get('email')
                b.phone = i.get('billing').get('phone')
                b.save()
                o.billing = b
            if i.get('shipping'):
                try:
                    s = Shipping.objects.get(email=i.get('shipping').get('email'))
                except Exception:
                    s = Shipping()
                s.id = i.get('shipping').get('id')
                s.first_name = i.get('shipping').get('first_name')
                s.last_name = i.get('shipping').get('last_name')
                s.company = i.get('shipping').get('company')
                s.address_1 = i.get('shipping').get('address_1')
                s.address_2 = i.get('shipping').get('address_2')
                s.city = i.get('shipping').get('city')
                s.state = i.get('shipping').get('state')
                s.postcode = i.get('shipping').get('postcode')
                s.country = i.get('shipping').get('country')
                s.save()
                o.shipping = s
            o.payment_method = i.get('payment_method')
            o.payment_method_title = i.get('payment_method_title')
            o.transaction_id = i.get('transaction_id')
            if i.get('date_paid'):
                o.date_paid = pytz.utc.localize(datetime.strptime(i.get('date_paid'), '%Y-%m-%dT%H:%M:%S'))
            if i.get('date_paid_gmt'):
                o.date_paid_gmt = pytz.utc.localize(datetime.strptime(i.get('date_paid_gmt'), '%Y-%m-%dT%H:%M:%S'))
            if i.get('date_completed'):
                o.date_completed = pytz.utc.localize(datetime.strptime(i.get('date_completed'), '%Y-%m-%dT%H:%M:%S'))
            if i.get('date_completed_gmt'):
                o.date_completed_gmt = pytz.utc.localize(datetime.strptime(i.get('date_completed_gmt'), '%Y-%m-%dT%H:%M:%S'))
            o.cart_hash = i.get('cart_hash')
            o.save()
            if i.get('meta_data'):
                for x in i.get('meta_data'):
                    try:
                        m = MetaData.objects.get(key=x.get('key'))
                    except Exception:
                        m = MetaData()
                    m.key = x.get('key')
                    m.value = json.dumps(x.get('value'))
                    m.save()
                    o.meta_data.add(m)

            if i.get('line_items'):
                for x in i.get('line_items'):
                    try:
                        l = LineItem.objects.get(id=x.get('id'))
                    except Exception:
                        l = LineItem()
                    l.id = x.get('id')
                    l.name = x.get('name')
                    if x.get('product_id'):
                        try:
                            p = Product.objects.get(id=x.get('product_id'))
                            l.product_id = p
                        except Exception:
                            pass

                    l.variation_id = x.get('variation_id')
                    l.quantity = x.get('quantity')
                    l.tax_class = x.get('tax_class')
                    l.subtotal = x.get('subtotal')
                    l.subtotal_tax = x.get('subtotal_tax')
                    l.total = x.get('total')
                    l.total_tax = x.get('total_tax')

                    if x.get('taxes'):
                        for y in x.get('taxes'):
                            try:
                                tl = TaxLine.objects.get(id=y.get('id'))
                            except Exception:
                                tl = TaxLine()
                            tl.rate_code = y.get('rate_code')
                            tl.rate_id = y.get('rate_id')
                            tl.label = y.get('label')
                            tl.compound = y.get('compound', False)
                            tl.tax_total = y.get('tax_total')
                            tl.shipping_tax_total = y.get('shipping_tax_total')
                            l.taxes.add(tl)

                    if x.get('meta_data'):
                        for y in x.get('meta_data'):
                            try:
                                m = MetaData.objects.get(key=y.get('key'))
                            except Exception:
                                m = MetaData()
                            m.key = y.get('key')
                            m.value = json.dumps(y.get('value'))
                            m.save()
                            l.meta_data.add(m)

                    l.sku = x.get('sku')
                    l.price = x.get('price')

                    l.save()
                    o.line_items.add(l)

            if i.get('tax_lines'):
                for x in i.get('tax_lines'):
                    try:
                        tl = TaxLine.objects.get(id=x.get('id'))
                    except Exception:
                        tl = TaxLine()
                    tl.rate_code = x.get('rate_code')
                    tl.rate_id = x.get('rate_id')
                    tl.label = x.get('label')
                    tl.compound = x.get('compound', False)
                    tl.tax_total = x.get('tax_total')
                    tl.shipping_tax_total = x.get('shipping_tax_total')
                    tl.save()
                    o.tax_lines.add(tl)

            if i.get('shipping_lines'):
                for x in i.get('shipping_lines'):
                    try:
                        sl = ShippingLine.objects.get(id=x.get('id'))
                    except Exception:
                        sl = ShippingLine()
                    sl.method_title = x.get('method_title')
                    sl.method_id = x.get('method_id')
                    sl.total = x.get('total')
                    sl.total_tax = x.get('total_tax')
                    sl.taxes = models.ManyToManyField('TaxLine', blank=True)
                    if x.get('taxes'):
                        for y in x.get('taxes'):
                            try:
                                tl = TaxLine.objects.get(id=y.get('id'))
                            except Exception:
                                tl = TaxLine()
                            tl.rate_code = y.get('rate_code')
                            tl.rate_id = y.get('rate_id')
                            tl.label = y.get('label')
                            tl.compound = y.get('compound', False)
                            tl.tax_total = y.get('tax_total')
                            tl.shipping_tax_total = y.get('shipping_tax_total')
                            sl.taxes.add(tl)
                    if x.get('meta_data'):
                        for y in x.get('meta_data'):
                            try:
                                m = MetaData.objects.get(key=y.get('key'))
                            except Exception:
                                m = MetaData()
                            m.key = y.get('key')
                            m.value = json.dumps(y.get('value'))
                            m.save()
                            sl.meta_data.add(m)
                    sl.save()
                    o.shipping_lines.add(sl)

            if i.get('fee_lines'):
                for x in i.get('fee_lines'):
                    try:
                        fl = FeeLine.objects.get(id=x.get('id'))
                    except Exception:
                        fl = FeeLine()
                    fl.name = x.get('name')
                    fl.tax_class = x.get('tax_class')
                    fl.tax_status = x.get('tax_status')
                    fl.total = x.get('total', 0.00)
                    fl.total_tax = x.get('total_tax', 0.00)

                    if x.get('taxes'):
                        for y in x.get('taxes'):
                            try:
                                tl = TaxLine.objects.get(id=y.get('id'))
                            except Exception:
                                tl = TaxLine()
                            tl.rate_code = y.get('rate_code')
                            tl.rate_id = y.get('rate_id')
                            tl.label = y.get('label')
                            tl.compound = y.get('compound', False)
                            tl.tax_total = y.get('tax_total')
                            tl.shipping_tax_total = y.get('shipping_tax_total')
                            fl.taxes.add(tl)
                    if x.get('meta_data'):
                        for y in x.get('meta_data'):
                            try:
                                m = MetaData.objects.get(key=y.get('key'))
                            except Exception:
                                m = MetaData()
                            m.key = y.get('key')
                            m.value = json.dumps(y.get('value'))
                            m.save()
                            fl.meta_data.add(m)

                    fl.save()
                    o.fee_lines.add(fl)

            if i.get('coupon_lines'):
                for x in i.get('coupon_lines'):
                    try:
                        cl = CouponLine.objects.get(id=x.get('id'))
                    except Exception:
                        cl = CouponLine()

                    cl.code = x.get('code')
                    cl.discount = x.get('discount')
                    cl.discount_tax = x.get('discount_tax')

                    if x.get('meta_data'):
                        for y in x.get('meta_data'):
                            try:
                                m = MetaData.objects.get(key=y.get('key'))
                            except Exception:
                                m = MetaData()
                            m.key = y.get('key')
                            m.value = json.dumps(y.get('value'))
                            m.save()
                            cl.meta_data.add(m)

                    cl.save()
                    o.coupon_lines.add(cl)

            if i.get('refunds'):
                for x in i.get('refunds'):
                    try:
                        r = Refund.objects.get(id=x.get('id'))
                    except Exception:
                        r = Refund()

                    r.reason = x.get('reason')
                    r.total = x.get('total', 0.0)

                    if x.get('meta_data'):
                        for y in x.get('meta_data'):
                            try:
                                m = MetaData.objects.get(key=y.get('key'))
                            except Exception:
                                m = MetaData()
                            m.key = y.get('key')
                            m.value = json.dumps(y.get('value'))
                            m.save()
                            r.meta_data.add(m)

                    r.save()
                    o.refunds.add(r)

    except Exception as err:
        return str(err)
    return True