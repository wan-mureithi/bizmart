from . import views
from django.conf.urls import url,include

#app_name = 'business'

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^admin-index',views.admin_index, name='admin-index'),
    url(r'^user_profile',views.user_prof, name='userprofile'),
    url(r'^collections',views.collections_all, name='collections'),
    url(r'^evaluation',views.evaluation, name='evaluation'),
    url(r'^collection-new',views.collection_new, name='collection-new'),
    url(r'^products',views.products_all, name='products'),
    url(r'^product_detail/(?P<id>[0-9]+)/',views.view_product, name='product-detail'),
    url(r'^customer-new',views.customer_new, name='customer-new'),
    url(r'^customers',views.customers_all, name='customers'),
    url(r'^customer-edit/(?P<id>[0-9]+)/',views.customer_edit, name='customer-edit'),
    url(r'^customer-delete/(?P<id>[0-9]+)/',views.customer_delete, name='customer-delete'),

    url(r'^invoice/(?P<id>[0-9]+)/',views.invoice, name='invoice'),
    url(r'^orders',views.orders_all, name='orders'),
    url(r'^mstOrder_edit/(?P<id>[0-9]+)/',views.mstOrder_edit, name='mstOrder_edit'),
    url(r'^orderDtl_edit/(?P<id>[0-9]+)/',views.orderDtl_edit, name='orderDtl_edit'),
    url(r'^order/(?P<id>[0-9]+)/',views.view_orders, name='order_detail'),
    url(r'^order-delete/(?P<id>[0-9]+)/',views.order_delete, name='order-delete'),
    url(r'^order-new',views.new_order, name='order-new'),
    url(r'^orderdtl_delete/(?P<id>[0-9]+)',views.orderdtl_delete, name='orderdtl_delete'),
    url(r'^recommendation',views.revenues_all, name='recommendation'),
    url(r'^social_metrics/',views.social_metrics, name='social_metrics'),
    url(r'^social_metrics_api/',views.social_metrics_api, name='social_metrics_api'),



    url(r'^income$',views.income_list, name='income'),
    url(r'^income_new/',views.income_new, name='income_new'),
    url(r'^income_edit/(?P<id>[0-9]+)/',views.income_edit, name='income_edit'),
    url(r'^income_delete/(?P<id>[0-9]+)/',views.income_delete, name='income_delete'),
    url(r'^costs',views.cost_list, name='costs'),
    url(r'^cost_new',views.cost_new, name='cost_new'),
    url(r'^cost_edit/(?P<id>[0-9]+)/',views.cost_edit, name='cost_edit'),
    url(r'^cost_delete/(?P<id>[0-9]+)/', views.cost_delete, name='cost_delete'),
    url(r'^finance_analysis/',views.finance_analytics, name='finance_analysis'),
    url(r'^error_404_demo', views.error_404, name='error_404_demo'),
    url(r'^error_500_demo', views.error_500, name='error_500_demo'),

]