# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product,Collection,ProductImage,Customer,OrderDtl,MstOrder,Creditors,CompanyProfile,Revenue,Costs,Expense_type
from .forms import CustomerForm,MstOrderForm,OrderDtlForm, CostsForm,RevenueForm,CreditorForm
from django.views.generic import ListView,DetailView
from django.contrib import messages


@login_required( login_url = '/accounts/login/')
def index(request):
    template_name = 'manager/index.html'
    return render(request,template_name)


def products_all(request):
    products = Product.objects.all()
    context = {'products': products}
    # product = Product.objects.get(id=id)
    # images = ProductImage.objects.filter(product=product)
    # args = {
    #     'product': product,
    #     'images': images,
    #     'success': False
    # }
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

def creditors_all(request):
    creditors = Creditors.objects.all()
    context = {'creditors':creditors}
    template_name = 'manager/customers/creditors_list.html'
    return render(request,template_name,context)

def creditor_new(request):
    template_name = 'manager/customers/creditor_new.html'

    if request.method == "POST":
        form = CreditorForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('creditors')
            except:
                pass
    else:
        form = CreditorForm()
    return render(request,template_name,{'form':form})

def customer_new(request):
    form = CustomerForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('customers')
    template_name = 'manager/customers/customer_new.html'
    return render(request,template_name,{'form':form})


def customers_all(request):
    customers = Customer.objects.all()
    context = {'customers':customers}
    template_name = 'manager/customers/customer_list.html'
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
    cust = get_object_or_404(Customer,id=id)
    try:
        if request.method =='POST':
            form = CustomerForm(request.POST,instance=cust)
            cust.delete()
            messages.success(request,'you have done it')
        else:
            form = CustomerForm(instance=cust)
    except Exception as e:
        messages.warning(request,'could not be deleted')

    context = {
        'form':form,
        'cust':cust,

    }    
    template_name = 'manager/customer_delete.html'
    return render(request, template_name,context)

class CustomerList(ListView):
    model = Customer
    template_name = 'manager/customers/customer_list.html'


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
    context = {'orders':orders}
    template_name = 'manager/order_list.html'
    return render(request,template_name,context)

'''def new_order(request):
    template_name = 'new_order.html'
    if request.method = "POST":

    else:
        mstOrder_form = MstOrderForm()
        orderdtl_form = OrderDtlForm()
    args = {}
    args.update(csrf(request))
    args['mstOrder_form'] = mstOrder_form
    args['orderdtl_form'] = orderdtl_form

    return render(request,template_name,args)'''

def mstOrder_new(request):
    form = MstOrderForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('orders')
    template_name = 'manager/new_order.html'
    return render(request,template_name,{'form':form})


def orderdtl_new(request):
    form = OrderDtlForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('orders')
    template_name = 'manager/orderdtls_new.html'
    return render(request,template_name,{'form':form})


class OrderdtlList(ListView):
    model = OrderDtl

class OrderDtlDetail(DetailView):
    model = MstOrder
    template_name = 'manager/view_order.html'


class MstOrderList(ListView):
    model = MstOrder
    template_name = 'manager/order_list.html'

def view_orders(request,id):
    #orderdtl = OrderDtl.objects.get(id=id)
    #mstOrder = MstOrder.objects.filter(orderdtl=)
    mstOrder = MstOrder.objects.get(id=id)
    orderdtl = OrderDtl.objects.filter(mstOrder=mstOrder)
    args = {
        'mstOrder': mstOrder,
        'orderdtl': orderdtl,
        'success': False
    }
    template_name = 'manager/view_order.html'
    return render(request,template_name,args)

def invoice(request,id):
    template_name = 'manager/invoice.html'
    return render(request,template_name)


def orderdtl(request):
    form = MstOrderForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('orders')
    template_name = 'manager/order_dtls.html'
    return render(request,template_name,{'form':form})

def user_prof(request,pk=None):
   
    profile = CompanyProfile.objects.get(pk=1)
   
    context = {'profile':profile}
    template_name = 'manager/profile.html'
    return render(request,template_name,context)

def revenues_all(request):
    template_name = 'manager/Finance/revenue.html'
    return render(request,template_name)

def expenses_all(request):
    template_name = 'manager/Finance/revenue.html'
    return render(request,template_name)

def cost_list(request):
    costs = Costs.objects.all()
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
    return render(request,template_name)


def cost_edit(request, id):
    instance = get_object_or_404(Costs, id=id)
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
    cost = get_object_or_404(Costs, id=id)
    cost.delete()
    messages.success(request,"successfully deleted")
    return redirect("costs")

def expense_detail(request,id):
    template_name = 'manager/Finance/expensetype_list.html'
    expense = Expense_type.objects.get(id=id)
    costs = Costs.objects.filter(expense=expense)
    args = {
        'expense': expense,
        'costs': costs,
        'success': False
    }
    return render(request,template_name,args)

#income

def income_new(request):
    form = RevenueForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('income')
    template_name = 'manager/Finance/income_new.html'
    return render(request, template_name, {'form': form})


def income_list(request):
    revenues = Revenue.objects.all()
    context = {'revenues': revenues}
    template_name = 'manager/income_list.html'
    return render(request, template_name, context)


def income_edit(request, id):
    instance = get_object_or_404(Revenue, id=id)
    form = RevenueForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        # print form.clean_data.get("cust_name")
        instance.save()
        return redirect('income')

    context = {
        "revenue": instance.revenue,  #column in the table
        "instance": instance,
        "form": form,
    }
    template_name = 'manager/Finance/income_edit.html'
    return render(request, template_name, context)


def income_delete(request,id):
    income = get_object_or_404(Revenue, id=id)
    income.delete()
    messages.success(request,"successfully deleted")
    return redirect("income")


