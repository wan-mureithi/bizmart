from django import forms
from .models import (Collection, OrderDtl, Customer, MstOrder, Cost,
                     Reward, Income )


class DateInput(forms.DateInput):
    input_type = 'date'

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'description', 'slug', 'date_created']


class CustomerForm(forms.ModelForm):
    #contact = forms.RegexField(regex=r'^\+?1?\d{10,15}$', error_messages={'required': 'Enter valid number'},)
    date_registered = forms.DateField(widget=DateInput)
    #date_registered = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))
    class Meta:
        model = Customer

        fields = ['cust_name','username','contact','secondary_contact','registered_from','date_registered']


# class InvoiceForm(forms.ModelForm):
#      invoice_date = forms.DateField(widget=DateInput)
#      complete_payment = forms.DateField(widget=DateInput)
#      class Meta:
#          model =
#          fields = ['mstOrder','invoice_date','discount','total_amount','customer','buy_on_credit','complete_payment']




class MstOrderForm(forms.ModelForm):
    date_ordered = forms.DateField(widget=DateInput)
    delivery_date = forms.DateField(widget=DateInput)
    class Meta:
        model = MstOrder
        fields = ['customer','date_ordered', 'staff', 'status']


class OrderDtlForm(forms.ModelForm):
    class Meta:
        model = OrderDtl
        fields = ['mstOrder','product', 'quantity', 'details']


class CostsForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ['amount', 'cost_date', 'staff']

class RewardForm(forms.ModelForm):
    date_awarded = forms.DateField(widget=DateInput)
    class Meta:
        model = Reward
        fields = ['staff', 'duration', 'date_awarded', 'assessment','amount_awarded']


class IncomeForm(forms.ModelForm):

    pay_date = forms.DateField(widget=DateInput)
    class Meta:
        model = Income
        fields = ['pay_date', 'amount_collected', 'payment_mode', 'collected_by','description']

