# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import datetime
import uuid
from django.db.models.signals import post_save

#func to restrict future dates
def no_future(value):
    today = date.today()
    if value > today:
        raise ValidationError('Date cannot be in the future.')

class CompanyProfile(models.Model):
    business_name = models.CharField(max_length=50)
    company_logo = models.ImageField(upload_to='img/profile_image',blank=True)
    description = models.TextField()
    website = models.URLField(default='')
    location = models.CharField(max_length=100,blank=True,null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    contact = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.CharField(max_length=50)

    def __unicode__(self):
        return self.business_name

class Staff(models.Model):
    user = models.OneToOneField(User)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    contact = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    employment_date = models.DateField(validators=[no_future])
    st_role = models.CharField(max_length=50)
    st_roledesc = models.TextField()
    st_image = models.ImageField(upload_to='img/staff',blank=True)

    def __unicode__(self):
        return self.user.username




class Collection(models.Model):
    title = models.CharField(max_length=50, null=False,blank=False)
    description = models.TextField(null=True)
    slug = models.SlugField(max_length=100, unique=True)
    date_created = models.DateField()

    def __unicode__(self):
        return self.title #must be a string

class Product(models.Model):
    collection = models.ForeignKey(Collection) #onetomanyrlshp
    title = models.CharField(max_length=120, null=False,blank=False) #blank is for the frontend(Please enter field)
    description = models.TextField(null=True)
    buying_price = models.BigIntegerField(null=False,blank=False)
    sale_price = models.BigIntegerField(null=False,blank=False)
    slug = models.SlugField(max_length=100, null=True)
    quantity = models.IntegerField(default=1)
    stock_date = models.DateField(default=True)
    #date_added = models.DateField()
    #updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_available = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.title



class ProductImage(models.Model):
    product = models.ForeignKey(Product) #many to one relationship. One product can have many images
    image = models.ImageField(upload_to='img/products')
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    #updated = models.DateTimeField(auto_now_add=False, auto_now=True)

REGISTRATION = (
    ('instagram', 'instagram'),
    ('facebook', 'facebook'),
    ('twitter', 'twitter'),
    ('ref', 'referral'), #another cust
    ('in_per', 'in_person'),  #seller  introduced you
)

class Customer(models.Model):
    cust_name = models.CharField(max_length=70,null=False,blank=True)
    username = models.CharField(max_length=70,null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    contact = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    secondary_contact = models.CharField(max_length=120,null=True)
    registered_from = models.CharField(max_length=20,choices=REGISTRATION)
    date_registered = models.DateField(validators=[no_future])
    gender = models.CharField(max_length=10,null=True)
    

    def __unicode__(self):
        return self.cust_name


    def get_absolute_url(self): #to redirect to a detail view
        return reverse('customer-edit', kwargs={'pk': self.pk})

STATUS = (
    ('Pending', 'Pending'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),    
)

#auto inc order no

def increment_order_number():
    last_order = MstOrder.objects.all().order_by('id').last()
    if not last_order:
         return 'ORD0001'
    order_no = last_order.orderNo
    order_int = int(order_no.split('ORD0')[-1])
    new_order_int = order_int + 1
    new_order_no = 'ORD0' + str(new_order_int)
    return new_order_no

#Parent table
class MstOrder(models.Model):
    customer = models.ForeignKey(Customer)
    orderNo = models.CharField(max_length=150,  default=increment_order_number, unique=True)  # lambda:str('ORD-'+str(uuid.uuid4().time_low))
    #invoiceNo = models.CharField(max_length=100,)
    date_ordered = models.DateField(validators=[no_future]) #you cannot order sth in the future
    discount = models.BigIntegerField(default=0)
    total_amount = models.BigIntegerField(default=0)
    buy_on_credit = models.BooleanField(default=False)  # initially false
    complete_payment = models.DateField(null=True, blank=True)  # when will they finish paying
    staff = models.ForeignKey(Staff)
    status = models.CharField(max_length=20,choices=STATUS) #delivered or not or cancelled

    def __unicode__(self):
        return self.orderNo


#child table (one to many)
class OrderDtl(models.Model):
    mstOrder = models.ForeignKey(MstOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,default=True)
    quantity = models.IntegerField(default=1)
    details = models.TextField()

    def __unicode__(self):
        return self.mstOrder.orderNo




FREQ = (
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Monthly', 'Monthly'),
    ('Quarterly', 'Quarterly'),
    ('Annually', 'Annually'),    
)

STATUS2 = (
    ('Partial','Partially paid'),
    ('Fully_paid','Fully Paid'),
    ('Not_paid','Not Paid'),
)

PAY = (
    ('cash','Cash'),
    ('Mpesa','Mpesa'),
)
def increment_invoice_number():
    last_invoice = MstOrder.objects.all().order_by('id').last()
    if not last_invoice:
         return 'INVO001'
    invoice_no = last_invoice.invoice_no
    invoice_int = int(invoice_no.split('INVO')[-1])
    new_invoice_int = invoice_int + 1
    new_invoice_no = 'INVO' + str(new_invoice_int)
    return new_invoice_no


class deliveries_tbl(models.Model):
    mstOrder = models.OneToOneField(MstOrder,related_query_name='order_deliv')
    delivery_date = models.DateField()
    delivery_location = models.CharField(max_length=100)
    delivery_fee = models.BigIntegerField()
    staff_to_deliver = models.ForeignKey(Staff)

    def __unicode__(self):
        return self.mstOrder.orderNo


class Income(models.Model):
    mstOrder = models.ForeignKey(MstOrder)
    pay_date = models.DateField()
    amount_collected = models.IntegerField()
    payment_mode = models.CharField(max_length=20,choices=PAY)
    collected_by = models.ForeignKey(Staff)
    description = models.TextField(null=True,blank=True)


    def __unicode__(self):
        return self.mstOrder.orderNo

# class IncomeSummary(Income):
#     class Meta:
#         verbose_name = 'Income Summary'
#         verbose_name_plural = 'Incomes Summary'



class Cost(models.Model):
    amount = models.IntegerField()
    cost_date = models.DateField()
    staff = models.ForeignKey(Staff) #who spent this money
    title = models.CharField(max_length=20,default='Expense')
    cost_purpose = models.TextField(null=True,default=' ')



    def __unicode__(self):
        return self.title


class Revenue(models.Model):
    rev_amount = models.IntegerField()
    rev_date = models.DateField()
    rev_desc = models.TextField(null=True)
    staff = models.ForeignKey(Staff)
    rv_title = models.CharField(max_length=20,default=' ')

    def __unicode__(self):
        return self.rv_title

class Budget(models.Model):
    purpose = models.CharField(max_length=20)
    description = models.TextField(null=True)
    amount = models.IntegerField()
    frequency = models.CharField(max_length=20,choices=FREQ)
    date_set = models.DateField()
    status = models.CharField(max_length=10)

    def __unicode__(self):
        return self.purpose

class Reward(models.Model):
    staff = models.ForeignKey(Staff,related_query_name='staff_reward')
    duration = models.CharField(max_length=15)
    date_awarded = models.DateField()
    assessment = models.TextField()
    amount_awarded = models.IntegerField()

    def __unicode__(self):
        return self.staff.user.username

class fb_metrics(models.Model):
    page_total_likes = models.BigIntegerField()
    post_type = models.CharField(max_length=10)
    post_month = models.IntegerField()
    post_weekday = models.IntegerField()
    post_hour = models.IntegerField()
    paid = models.BooleanField(default=False)
    post_consumers = models.IntegerField()
    total_interactions = models.IntegerField()

    def __unicode__(self):
        return self.post_type








    



