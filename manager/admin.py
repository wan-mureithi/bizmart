# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Collection, Product, ProductImage, Customer,MstOrder,OrderDtl,Staff,Expense_type,Costs,CompanyProfile, Revenue,Revenue_type


admin.site.site_header = 'Smart Biz'

class ProductAdmin(admin.ModelAdmin):
   # date_hierarchy = 'updated' #should be a dateTime field for accuracy
    search_fields = ['title','description']
    list_display = ['title','buying_price','sale_price','is_available','updated']
    list_editable = ['buying_price','is_available']
    list_filter = ['buying_price','is_available']
    readonly_fields = ['updated']

class CustomerAdmin(admin.ModelAdmin):
   # date_hierarchy = 'updated' #should be a dateTime field for accuracy
    search_fields = ['cust_name','username']
    list_display = ['cust_name','contact','registered_from','date_registered']
    list_editable = ['contact']
    list_filter = ['registered_from','date_registered']
    #readonly_fields = ['updated']

class MstOrderAdmin(admin.ModelAdmin):
   # date_hierarchy = 'updated' #should be a dateTime field for accuracy
    search_fields = ['cust_name','username']
    list_display = ['customer','orderNo','total_price','staff','status','delivery_date','date_ordered']
    list_editable = ['date_ordered','status']
    list_filter = ['status','delivery_date']

admin.site.register(Collection)
admin.site.register(CompanyProfile)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(MstOrder,MstOrderAdmin)
admin.site.register(OrderDtl)
admin.site.register(Staff)
admin.site.register(Revenue)
admin.site.register(Revenue_type)
admin.site.register(Expense_type)
admin.site.register(Costs)
