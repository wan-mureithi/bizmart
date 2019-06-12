# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ( Staff, Product,Collection,ProductImage,Customer,OrderDtl,MstOrder,deliveries_tbl,
                      CompanyProfile,Revenue,Cost, Income, Reward,fb_metrics)
from .forms import (CustomerForm,MstOrderForm,OrderDtlForm,RewardForm,
                    CostsForm, IncomeForm )
from django.db.models import Count, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Count, Q, Sum, Case, When,IntegerField,ExpressionWrapper
from django.db.models.functions import TruncMonth, ExtractWeek
from django.contrib.auth.models import User
import datetime
import operator
from django.http import JsonResponse
import pandas as pd


def clean_datas(data):
    months = []
    for d in data:
        months.append(d['month'].month)
    for i in range(12):
        if i+1 not in months:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
            data.append({'count':0, 'month': datetime.date(2018, i+1, 1)})

    return sorted(data, key=operator.itemgetter('month'))


#X_train, X_test, y_train, y_test = train_test_split(x_features, y, test_size=0.2)
def social_metrics(request):
    fb_data = fb_metrics.objects.all()
    # counts the instances for every type of post
    post_types =fb_metrics.objects.values('post_type').annotate(count=Count('post_type')).order_by('post_type')
    good_days = fb_metrics.objects.values('post_weekday').annotate(count=Count('post_weekday')).order_by('post_weekday')
    arg = {
        'post_types':post_types,
        'good_days': good_days,

    }

    print(good_days)

    template_name = 'manager/social_metrics.html'
    return render(request,template_name,arg)

def social_metrics_api(request):
    values = []

    post_types =fb_metrics.objects.values('post_type').annotate(count=Count('post_type')).order_by('post_type')
    #print( post_types['count'])
    post_types.count
    for i in post_types:
        # print(i['count'])
        # print(i['post_type'])
        ccount = i['count']
        posttype = i['post_type']

        arg = {
            'name': posttype,
            'y':ccount

        }
        values.append(arg)
    print(arg)

    template_name = 'manager/social_metrics.html'
    return JsonResponse(values, safe = False)




@login_required( login_url = '/accounts/login/')
def index(request):
    user = request.user

    sale = Income.objects.filter(collected_by=user.id)
    sales = sale.annotate(month=TruncMonth('pay_date'), ).values('month').annotate(
        count=Sum('amount_collected')).order_by('month')
    staff_deliveries = deliveries_tbl.objects.filter(staff_to_deliver=user.id)
    sub = staff_deliveries.annotate(month=TruncMonth('delivery_date'), ).values('month').annotate(
        count=Count('mstOrder_id')).order_by('month')
    deliv = clean_datas(list(sub))
    staff_orders = MstOrder.objects.filter(staff=user.id)
    sub4 = staff_orders.annotate(month=TruncMonth('date_ordered'), ).values('month').annotate(
        count=Count('orderNo')).order_by('month')
    orders4 = clean_datas(list(sub4))
    staff_costs = Cost.objects.filter(staff=user.id)
    costs = staff_costs.annotate(month=TruncMonth('cost_date'), ).values('month').annotate(
        count=Sum('amount')).order_by('month')

    arg = {
        'sales':sales,
        'costs': costs,
        'deliv': deliv,

        'orders4': orders4,

    }
    #print (all_monies)
    template_name = 'manager/index.html'
    return render(request,template_name,arg)

def admin_index(request):
    staffs = Staff.objects.all()
    orders = MstOrder.objects.all()
    all_orders = orders.annotate(month=TruncMonth('date_ordered')).values('month').annotate(total=Count('date_ordered'))
    deliveries = deliveries_tbl.objects.filter(staff_to_deliver=1, )
    #all = deliveries.annotate(month=TruncMonth('delivery_date')).values('month').annotate(total=Count('id'))

    delivery = deliveries_tbl.objects.filter(staff_to_deliver__user__is_superuser=False)
    queried =  delivery.annotate(week=ExtractWeek('delivery_date')).values('week','staff_to_deliver__user__username').annotate(total=Count('mstOrder_id'))
    arg = {
        'queried':queried,
    }
    template_name = 'manager/index2.html'
    return render(request, template_name,arg)
#      [x['staff_to_deliver__user__id'],x['week'],x['total']] for x in queried ]


def evaluation(request):
    staff1_deliveries = deliveries_tbl.objects.filter(staff_to_deliver=1)
    sub1 = staff1_deliveries.annotate(month=TruncMonth('delivery_date'), ).values('month').annotate(
        count=Count('pk')).order_by('month')

    s1 = clean_datas(list(sub1))  # add the zero count and make sure everything is okay
    staff1_costs = Cost.objects.filter(staff=1)
    cost1 = staff1_costs.annotate(month=TruncMonth('cost_date'), ).values('month').annotate(
        count=Sum('amount')).order_by('month')

    #shows deliveries for all non superusers in Nov
    delivery = deliveries_tbl.objects.filter(staff_to_deliver__user__is_superuser=False, delivery_date__month=11)

        #sub counts all deliveries done monthly(by all staff)
    staff4_deliveries = deliveries_tbl.objects.filter(staff_to_deliver=4)
    sub4=staff4_deliveries.annotate(month=TruncMonth('delivery_date'),).values('month').annotate(count=Count('mstOrder_id')).order_by('month')
    s4 = clean_datas(list(sub4))
    staff4_costs = Cost.objects.filter(staff=4)
    cost4 = staff4_costs.annotate(month=TruncMonth('cost_date'), ).values('month').annotate(
        count=Sum('amount')).order_by('month')

    staff2_deliveries = deliveries_tbl.objects.filter(staff_to_deliver=2)
    sub2 = staff2_deliveries.annotate(month=TruncMonth('delivery_date'), ).values('month').annotate(
        count=Count('pk')).order_by('month')
    s2 = clean_datas(list(sub2))
    staff2_costs = Cost.objects.filter(staff=2)
    cost2 = staff2_costs.annotate(month=TruncMonth('cost_date'), ).values('month').annotate(
        count=Sum('amount')).order_by('month')

    staff3_deliveries = deliveries_tbl.objects.filter(staff_to_deliver=3)
    sub3 = staff3_deliveries.annotate(month=TruncMonth('delivery_date')).values('month').annotate(
        count=Count('mstOrder_id')).order_by('month')
    s3 = clean_datas(list(sub3))
    staff3_costs = Cost.objects.filter(staff=3)
    cost3 = staff3_costs.annotate(month=TruncMonth('cost_date'), ).values('month').annotate(
        count=Sum('amount')).order_by('month')


    staff5_deliveries = deliveries_tbl.objects.filter(staff_to_deliver=5)
    sub5 = staff5_deliveries.annotate(month=TruncMonth('delivery_date'), ).values('month').annotate(
        count=Count('mstOrder_id')).order_by('month')
    s5 = clean_datas(list(sub5))
    staff5_costs = Cost.objects.filter(staff=5)
    cost5 = staff5_costs.annotate(month=TruncMonth('cost_date'), ).values('month').annotate(
        count=Sum('amount')).order_by('month')

    orders = MstOrder.objects.all()
    order_query = orders.annotate(month=TruncMonth('date_ordered')).values('month').annotate(
        total=Count('orderNo')).order_by('month')
    deliv_query = deliveries_tbl.objects.annotate(month=TruncMonth('delivery_date')).values('month').annotate(
        total=Count('mstOrder')).order_by('month')
    expenses = Cost.objects.annotate(month=TruncMonth('cost_date')).values('month').annotate(some=Sum('amount')).order_by('month')
    #print(expenses)
    #print('good stuff',cost1)

    form = RewardForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('evaluation')

    rewards = Reward.objects.all()

    arg = {
        'order_query': order_query,
        'deliv_query': deliv_query,
        's4':s4, 'cost4':cost4, 'cost3': cost3, 'cost2':cost2, 'cost1': cost1, 'cost5': cost5,
        's3': s3,
        's2': s2,
        's1': s1,
        's5': s5,
        'form': form,
        'rewards': rewards,

    }
    template_name = 'manager/evaluation.html'
    return render(request, template_name, arg)


def products_all(request):
    products = Product.objects.all()
    paginator = Paginator(products, 5)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    context = {
        'products': products,
        'items': items,
        'page_range': page_range,
    }

    template_name = 'manager/products/product_list.html'
    return render(request, template_name, context)

def view_product(request,id):
     product = Product.objects.get(id=id)
     images = ProductImage.objects.filter(product=product)
     args = {
         'product': product,
         'images': images,
         'success': False
     }
     template_name = 'manager/products/product_detail.html'
     return render(request,template_name,args)




def customer_new(request):
    form = CustomerForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('customers')
    template_name = 'manager/customers/customer_new.html'
    return render(request,template_name,{'form':form})


def customers_all(request):
    customers = Customer.objects.all()
    template_name = 'manager/customers/customer_list.html'
    paginator = Paginator(customers, 20)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)



    context = {
        'customers': customers,
        'items':items,
        # 'page_range': page_range,
    }
    return render(request,template_name,context)

def customer_edit(request,id=None):
    instance = get_object_or_404(Customer,id=id)
    form = CustomerForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
       # print form.clean_data.get("cust_name")
        instance.save()
        return redirect('customers')

    context = {
        "cust_name":instance.cust_name,
        "instance":instance,
        "form":form,
    }
    template_name = 'manager/customers/customer_edit.html'
    return render(request,template_name,context)

def customer_delete(request,id=None):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    messages.success(request, "successfully deleted")
    return redirect("customers")

#practice func
def invoices(request):
    some_data = Customer.objects.all()
    template_name = 'invoice_list.html'
    return render(request,template_name)
def collections_all(request):
    collections = Collection.objects.all()
    context = {'collections':collections}
    template_name = 'manager/collection_list.html'
    return render(request,template_name,context)

def collection_new(request):
    template_name = 'manager/collection_list.html'
    return render(request,template_name)

def orders_all(request):
    orders = MstOrder.objects.all()

    context = {
        'orders':orders,

    }
    template_name = 'manager/order_list.html'
    return render(request,template_name,context)

def order_delete(request,id):
    order = get_object_or_404(Revenue, id=id)
    order.delete()
    messages.success(request, "successfully deleted")
    return redirect("orders")



def view_orders(request,id):
    mstOrder = MstOrder.objects.get(id=id)
    orders =OrderDtl.objects.all()
    #product = Product.objects.get(id=id)
    orderdtl = OrderDtl.objects.filter(mstOrder=mstOrder)
    delivery_details = deliveries_tbl.objects.filter(mstOrder=mstOrder)
    #stuff = MstOrder.objects.select_related('staff').filter(mstOrder)
    OrderDtl.objects.aggregate(total_products=Count('id',filter=orderdtl))
    # amount = orderdtl.annotate(amount = F('quantity')*2)
    args = {
        'mstOrder': mstOrder,
        'orderdtl': orderdtl,
        'delivery_details': delivery_details,

        #'amount': amount,
        'success': False
    }
    template_name = 'manager/view_order.html'
    return render(request,template_name,args)

def order_payments(request,id):
    order = MstOrder.objects.get(id=id)
    payments = Income.objects.filter(mstOrder=order)
    delivery = deliveries_tbl.objects.filter(mstOrder=order)
    args = {
        'order': order,
        'payments':payments,
        'delivery': delivery,
    }

    template_name = 'manager/Finance/invoice_list.html'
    return render(request, template_name, args)

def invoice(request,id):
    mstOrder = MstOrder.objects.get(id=id)

    orderdtl = OrderDtl.objects.filter(mstOrder=mstOrder)
    company = CompanyProfile.objects.get(pk=1)
    delivery = deliveries_tbl.objects.filter(mstOrder=mstOrder)
    sub = orderdtl.annotate(s=ExpressionWrapper(F('quantity') * F('product__sale_price'),output_field=IntegerField()))

    args = {
        'mstOrder': mstOrder,
        'orderdtl': orderdtl,
        'company': company,
        'delivery': delivery,

        'success': False
    }
    print(sub)
    template_name = 'manager/invoice.html'
    return render(request,template_name,args)



#edit order details
def orderdtl(request):
    form = OrderDtlForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('orders')
    template_name = 'manager/order_dtls.html'
    return render(request,template_name,{'form':form})

def user_prof(request):

    user = request.user
    name = user.get_full_name()
    profile = CompanyProfile.objects.get(pk=1)
    staff = Staff.objects.get(id=user.id)

    staff_deliveries = deliveries_tbl.objects.filter(staff_to_deliver=user.id)
    sub = staff_deliveries.annotate(month=TruncMonth('delivery_date'), ).values('month').annotate(
        count=Count('mstOrder_id')).order_by('month')
    deliv = clean_datas(list(sub))
    staff_orders = MstOrder.objects.filter(staff=user.id)
    sub4 = staff_orders.annotate(month=TruncMonth('date_ordered'), ).values('month').annotate(
        count=Count('orderNo')).order_by('month')
    orders4 = clean_datas(list(sub4))

    rewards = Reward.objects.filter(staff=user.id) 
    context = {'profile':profile,
               'staff':staff, 'deliv': deliv, 'orders4': orders4,
               'name':name,}

    template_name = 'manager/profile.html'
    return render(request,template_name,context)

from scipy import mean
import numpy as np
xs = np.array([1,2,3,4,5,6,7,8,9,10,11,12],dtype=np.float64)
ys= np.array([31,71,54,73,52,48,54,87,58,63,91,86],dtype=np.float64)

def best_fit(xs,ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
        ((mean(xs)*mean(xs)) - mean(xs*xs)))

    b = mean(ys) - m * mean(xs)
    return m, b
def revenues_all(request):
    m, b = best_fit(xs, ys)
    #print(m, b)
    regression_line = [(m * x) + b for x in xs] #predicted ys
    x_values = xs
    y_values = ys
    #print(regression_line) #output

    data = Customer.objects.all().values().annotate(total=Count('id',filter=Q(registered_from='instagram'))).order_by('total')
    #deliveries = deliveries_tbl.objects.filter(staff_to_deliver=user, mstOrder__status='Delivered')
    #all = deliveries.annotate(month=TruncMonth('delivery_date')).values('month').annotate(total=Count('delivery_date'))
    template_name = 'manager/Finance/review.html'
    return render(request,template_name,{'regression_line': regression_line,'x_values':x_values,'y_values':y_values,})

def ticket_class_view(request):
    dataset = Income.objects \
        .values('customer_class') \
        .annotate(cash_payments=Count('payment_mode', filter=Q(payment_mode='cash')),
                  mpesa=Count('payment_mode', filter=Q(payment_mode='mpesa'))) \
        .order_by('pay_date')
    return render(request, 'review.html', {'dataset': dataset})



def cost_list(request):
    costs = Cost.objects.all()
    context = {'costs': costs}
    template_name = 'manager/Finance/cost_list.html'
    return render(request, template_name, context)


def cost_new(request):
    form = CostsForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('costs')
    template_name = 'manager/Finance/cost_new.html'
    return render(request, template_name, {'form': form})

def new_order(request):
    template_name = 'manager/products/create_order.html'
    if request.method == "POST":

        form = MstOrderForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('order-new')
            except:
                pass
    else:
        form = MstOrderForm()

    if request.method == "POST":
        form2 = OrderDtlForm(request.POST)
        if form2.is_valid():
            try:
                form2.save()
                return redirect('order-new')
            except:
                pass
    else:
        form2 = OrderDtlForm()
    args = {
        'form':form,
        'form2': form2,
    }
    return render(request, template_name,args)

def mstOrder_edit(request,id):
    instance = get_object_or_404(MstOrder, id=id)
    form = MstOrderForm(request.POST or None, instance=instance)
    mstOrder = MstOrder.objects.get(id=id)
    orderdtl = OrderDtl.objects.filter(mstOrder=mstOrder)
    if form.is_valid():
        instance = form.save(commit=False)

        instance.save()
        return redirect('orders')
    context = {
        'mstOrder':mstOrder,
        'orderdtl': orderdtl,
        'form': form,
        'instance': instance,
    }
    template_name = 'manager/products/mstOrder_edit.html'
    return render(request,template_name,context)

def get_data(request, *args, **kwargs):
    data = {
        "sales":100,
        "customers":10
    }
    return JsonResponse(data)



def orderDtl_edit(request,id):
    instance = get_object_or_404(OrderDtl, id=id)
    form = OrderDtlForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)

        instance.save()
        return redirect('order_detail')
    context = {
        'order': instance.mstOrder,
        'form': form,
        'instance': instance,
    }
    template_name = 'manager/products/orderDtl_edit.html'
    return render(request,template_name,context)

def orderdtl_delete(request,id):
    orderdtl = get_object_or_404(OrderDtl, id=id)
    orderdtl.delete()
    messages.success(request, "successfully deleted")
    return redirect("order_detail")



def cost_edit(request, id):
    instance = get_object_or_404(Cost, id=id)
    form = CostsForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        # print form.clean_data.get("cust_name")
        instance.save()
        return redirect('costs')

    context = {
        "expense": instance.expense,
        "instance": instance,
        "form": form,
    }
    template_name = 'manager/Finance/cost_update.html'
    return render(request,template_name, context)


def cost_delete(request,id):
    cost = get_object_or_404(Cost, id=id)
    cost.delete()
    messages.success(request,"successfully deleted")
    return redirect("costs")

def finance_analytics(request):
    #monies = Income.objects.filter()
    order_products = OrderDtl.objects.values('product__collection__title').annotate(count=Count('product__collection__title')).order_by('-count')
    expense_types = Cost.objects.values('title').annotate(total=Sum('amount')).order_by('title')

    expenses = Cost.objects.annotate(month=TruncMonth('cost_date')).values('month').annotate(
        some=Sum('amount')).order_by('month') # all monthly expesnses
    incomes = Income.objects.annotate(month=TruncMonth('pay_date')).values('month').annotate(
        some=Sum('amount_collected')).order_by('month')


    template_name = 'manager/Finance/analysis.html'
    y = []
    x = []
    for item in list(incomes):
        x.append(item['some'])
    for i in list(expenses):
        # print(i['some'])
        y.append(i['some'])

    profit =[]

    for a, b in zip(x,y):
        float(a)
        float(b)
        profit.append(((a-b)/a)*100) #profit = incomes.some - expenses.some
    #print(order_products)



    args = {
        'incomes': incomes,
        'profit': profit,
        'expenses': expenses,
        'expense_types': expense_types,
        'order_products': order_products,
    }

    return render(request, template_name, args)

#income

def income_new(request):
    form = IncomeForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('income')
    template_name = 'manager/Finance/income_new.html'
    return render(request, template_name, {'form': form})


def income_list(request):
    revenues = Income.objects.all()
    context = {'revenues': revenues}
    template_name = 'manager/Finance/income_list.html'
    return render(request, template_name, context)


def income_edit(request, id):
    instance = get_object_or_404(Income, id=id)
    form = IncomeForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        # print form.clean_data.get("cust_name")
        instance.save()
        return redirect('income')

    context = {
        "invoiceNo": instance.invoiceNo,  #column in the table
        "instance": instance,
        "form": form,
    }
    template_name = 'manager/Finance/income_edit.html'
    return render(request, template_name, context)


def income_delete(request,id):
    income = get_object_or_404(Income, id=id)
    income.delete()
    messages.success(request,"successfully deleted")
    return redirect("income")

#error handling
def error_404(request):
    data = {}
    return render(request, 'error_404.html', data)


def error_500(request):
    data = {}
    return render(request, 'error_500.html', data)