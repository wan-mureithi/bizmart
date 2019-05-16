# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class CompanyProfile(models.Model):
    business_name = models.CharField(max_length=50)
    company_logo = models.ImageField(upload_to='img/profile_image',blank=True)
    description = models.TextField()
    website = models.URLField(default='')
    contact = models.IntegerField(default=0)
    email = models.CharField(max_length=50)

    def __unicode__(self):
        return self.business_name

class Staff(models.Model):
    user = models.OneToOneField(User)
    st_name = models.CharField(max_length=50)
    st_username = models.CharField(max_length=50)
    employment_date = models.DateField()
    st_role = models.CharField(max_length=50)
    st_roledesc = models.TextField()
    st_image = models.ImageField(upload_to='img/staff',blank=True)

    def __unicode__(self):
        return self.st_username


# def create_staff(sender, **kwargs):
#     if kwargs['created']:
#         staff = Staff.objects.create(user=kwargs['instance'])
#
#     post_save.connect(create_staff,sender=User)


class Collection(models.Model):
    title = models.CharField(max_length=50, null=False,blank=False)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    date_created = models.DateField()

    def __unicode__(self):
        return self.title #must be a string

class Product(models.Model):
    collection = models.ForeignKey(Collection) #onetomanyrlshp
    title = models.CharField(max_length=120, null=False,blank=False) #blank is for the frontend(Please enter field)
    description = models.TextField()
    buying_price = models.BigIntegerField(null=False,blank=False)
    sale_price = models.BigIntegerField(null=False,blank=False)
    slug = models.SlugField(max_length=100, unique=True)
    quantity = models.BigIntegerField(null=True)
    date_added = models.DateField()
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
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
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

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
    contact = models.BigIntegerField()
    secondary_contact = models.CharField(max_length=120,null=True)
    registered_from = models.CharField(max_length=20,choices=REGISTRATION)
    date_registered = models.DateField()
    

    def __unicode__(self):
        return self.cust_name


    def get_absolute_url(self): #to redirect to a detail view
        return reverse('customer-edit', kwargs={'pk': self.pk})

STATUS = (
    ('Pending', 'Pending'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),    
)

#Parent table
class MstOrder(models.Model):
    customer = models.ForeignKey(Customer)
    orderNo = models.CharField(max_length=20,default='OrdNo11')
    date_ordered = models.DateField()
    delivery_date = models.DateField()
    delivery_location=models.CharField(max_length=50)
    delivery_fee = models.BigIntegerField(default=0)
    staff = models.ForeignKey(Staff)
    total_price = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)
    status = models.CharField(max_length=20,choices=STATUS) #delivered or not or cancelled

    def __unicode__(self):
        return self.orderNo

    def get_absolute_url(self):
        return reverse('mst_order-detail', kwargs={'pk': self.pk})

#child table (one to many)
class OrderDtl(models.Model):
    mstOrder = models.ForeignKey(MstOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,default=True)
    discount = models.BigIntegerField(default=0)
    details = models.TextField()

    def __unicode__(self):
        return self.mstOrder.orderNo

    def get_absolute_url(self):
        return reverse('order_dtl-edit', kwargs={'pk': self.pk})





class Sales(models.Model):
    saleNo = models.CharField(max_length=25,null=False)
    description = models.TextField(null=True)
    staff=models.ManyToManyField(Staff)
    amount = models.BigIntegerField()

    def __unicode__(self):
        return self.saleNo
#class company_profile(models.Model):
    
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
    ('Not_paid','Not Paid')
)

class Creditors(models.Model):
    customer = models.ForeignKey(Customer) 
    mstOrder = models.ForeignKey(MstOrder,null=True)
    amount_paid = models.BigIntegerField()
    description = models.TextField()
    payment_mode = models.CharField(max_length = 20)
    status = models.CharField(max_length=20,choices=STATUS2)
    date_paid = models.DateField()
    

    def __unicode__(self):
        return self.customer.username

class Expense_type(models.Model):
    ex_title =  models.CharField(max_length = 20)
    ex_frequency = models.CharField(max_length = 20,choices=FREQ)
    ex_purpose = models.CharField(max_length = 20)
    ex_datecreated = models.DateField()

    def __unicode__(self):
        return self.ex_title

class Costs(models.Model):
    expense = models.ForeignKey(Expense_type)
    amount = models.BigIntegerField()
    cost_date = models.DateField()
    staff = models.ForeignKey(Staff)
    cost_desc = models.TextField(null=True)

    def __unicode__(self):
        return self.expense.ex_title

class Revenue_type(models.Model):
    rv_title = models.CharField(max_length = 20)
    rv_datecreated = models.DateField()
    rv_frequency = models.CharField(max_length = 20,choices=FREQ)

    def __unicode__(self):
        return self.rv_title

class Revenue(models.Model):
    revenue = models.ForeignKey(Revenue_type)
    rev_amount = models.BigIntegerField()
    rev_date = models.DateField()
    rev_desc = models.TextField(null=True)
    staff = models.ForeignKey(Staff)

    def __unicode__(self):
        return self.revenue.rv_title

class budget(models.Model):
    purpose = models.CharField(max_length=20)
    description = models.TextField(null=True)
    amount = models.IntegerField()
    frequency = models.CharField(max_length=20,choices=FREQ)
    date_set = models.DateField()
    status = models.CharField(max_length=10)

    def __unicode__(self):
        return self.purpose







    



