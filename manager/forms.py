from django import forms
from .models import Collection, OrderDtl, Customer, MstOrder, Costs, Revenue, Creditors
#from .models import OrderDtl


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'description', 'slug', 'date_created']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['cust_name','username','contact','secondary_contact','registered_from','date_registered']


class CreditorForm(forms.ModelForm):
    class Meta:
        model = Creditors
        fields = ['customer','mstOrder','amount_paid','payment_mode','description','date_paid','status']


class MstOrderForm(forms.ModelForm):
    class Meta:
        model = MstOrder
        fields = ['customer','orderNo','date_ordered','delivery_date','delivery_location','delivery_fee','total_price','status']


class OrderDtlForm(forms.ModelForm):
    class Meta:
        model = OrderDtl
        fields = ['mstOrder','product','details','discount']


class CostsForm(forms.ModelForm):
    class Meta:
        model = Costs
        fields = ['expense', 'amount', 'cost_date', 'staff', 'cost_desc']

class RevenueForm(forms.ModelForm):
    class Meta:
        model = Revenue
        fields = ['revenue', 'rev_amount', 'rev_date', 'staff', 'rev_desc']
