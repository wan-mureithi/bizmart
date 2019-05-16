from . import views
from django.conf.urls import url,include

#app_name = 'business'

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^user_profile',views.user_prof, name='userprofile'),
    url(r'^collections',views.collections_all, name='collections'),
    url(r'^collection-new',views.collection_new, name='collection-new'),
    url(r'^products',views.products_all, name='products'),
    url(r'^product_detail/(?P<id>[0-9]+)/',views.view_product, name='product-detail'),
    url(r'^customer-new',views.customer_new, name='customer-new'),
    url(r'^customers',views.CustomerList.as_view(), name='customers'),
    url(r'^customer-edit/(?P<id>[0-9]+)/',views.customer_edit, name='customer-edit'),
    url(r'^customer-delete/(?P<id>[0-9]+)/',views.customer_delete, name='customer-delete'),
    url(r'^creditors',views.creditors_all, name='creditors'),
    url(r'^creditor_new',views.creditor_new, name='creditor_new'),
    url(r'^orders',views.orders_all, name='orders'),
    url(r'^order/(?P<id>[0-9]+)/',views.view_orders, name='order_detail'),
    url(r'^order-new',views.new_order, name='order-new'),
    url(r'^order-dtls',views.orderdtl_new, name='order-dtls'),
    url(r'^revenue',views.revenues_all, name='revenue'),
    url(r'^expenses',views.expenses_all, name='expenses'),
    url(r'^income$',views.income_list, name='income'),
    url(r'^income_new/',views.income_new, name='income_new'),
    url(r'^income_edit/(?P<id>[0-9]+)/',views.income_edit, name='income_edit'),
    url(r'^income_delete/(?P<id>[0-9]+)/',views.income_delete, name='income_delete'),
    url(r'^costs',views.cost_list, name='costs'),
    url(r'^cost_new',views.cost_new, name='cost_new'),
    url(r'^cost_edit/(?P<id>[0-9]+)/',views.cost_edit, name='cost_edit'),
    url(r'^cost_delete/(?P<id>[0-9]+)/', views.cost_delete, name='cost_delete'),
    url(r'^expense_detail/(?P<id>[0-9]+)/',views.expense_detail, name='expense_detail'),
]