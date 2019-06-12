# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (Collection, Product, ProductImage, Customer,MstOrder,
                      OrderDtl,Staff,Cost,CompanyProfile, deliveries_tbl,
                      Revenue,Income,Budget)
from django.db.models import Count, Sum

admin.site.site_header = 'Smart Biz'

class ProductAdmin(admin.ModelAdmin):
   # date_hierarchy = 'updated' #should be a dateTime field for accuracy
    search_fields = ['title','description']
    list_display = ['title','buying_price','sale_price','is_available']
    list_editable = ['buying_price','is_available']
    list_filter = ['sale_price','is_available']
#     #readonly_fields = ['updated']

class CustomerAdmin(admin.ModelAdmin):
   # date_hierarchy = 'updated' #should be a dateTime field for accuracy
    search_fields = ['cust_name','username']
    list_display = ['cust_name','contact','registered_from','date_registered']
    list_editable = ['contact','registered_from']
    list_filter = ['registered_from','date_registered']
    list_per_page = 20
    #readonly_fields = ['updated']

class ProductImageAdmin(admin.ModelAdmin):
   # date_hierarchy = 'updated' #should be a dateTime field for accuracy
   # search_fields = ['']
    list_display = ['product']
    list_per_page = 20

class MstOrderAdmin(admin.ModelAdmin):

    list_display = ['orderNo','customer','date_ordered']
    list_per_page = 20

class OrderDtlAdmin(admin.ModelAdmin):
    list_display = ['mstOrder','product','quantity']
    list_per_page = 20

class IncomeAdmin(admin.ModelAdmin):
    list_display = ['mstOrder','pay_date','amount_collected']
    list_per_page = 10



# class IncomeSummaryAdmin(admin.ModelAdmin):
#     change_list_template = 'admin/payment_summary_change_list.html'
#     date_hierarchy = 'pay_date'
#
#     def changelist_view(self, request, extra_context=None):
#         response = super().changelist_view(
#             request,
#             extra_context=extra_context,
#         )
#
#         try:
#             qs = response.context_data['cl'].queryset
#         except (AttributeError, KeyError):
#             return response
#
#         metrics = {
#         'total': Count('id'),
#         'total_sales': Sum('price'),
#         }
#
#         response.context_data['summary'] = list(
#             qs
#                 .values('sale__category__name')
#         .annotate(**metrics)
#             .order_by('-total_sales')
#         )
#
#         return response

admin.site.register(Collection)
admin.site.register(CompanyProfile)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage,ProductImageAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(MstOrder,MstOrderAdmin)
admin.site.register(OrderDtl,OrderDtlAdmin)
admin.site.register(Staff)
admin.site.register(Revenue)

admin.site.register(Cost)
admin.site.register(deliveries_tbl)
admin.site.register(Income,IncomeAdmin)
admin.site.register(Budget)
