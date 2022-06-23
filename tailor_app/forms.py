from django import forms
from .models import Customer, Order, Measurement, ExtraMeasurement
from django.utils import timezone

class CustomerForm(forms.ModelForm):
    class Meta:
        model =  Customer
        fields = ('name', 'email', 'sex', 'phone_no', 'address')


class EditCustomerForm(forms.ModelForm):
    class Meta:
        model =  Customer
        fields = ('id', 'name', 'email', 'sex', 'phone_no', 'address')

class OrderForm(forms.ModelForm):
    class Meta:
        model =  Order
        fields = ('customer',
        'quantity',
        'amount',
        'paid',
        'delivery_date',
        'description')
        widgets = {
            'delivery_date' : forms.DateInput(attrs = {"type":"date"})
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(tailor = self.request.user)

    def clean_paid(self):
        paid = self.cleaned_data.get("paid")
        amount = self.cleaned_data.get("amount")
        if paid > amount:
            raise forms.ValidationError('You can"t paid more than the initial amount')
        return  paid


    def clean_delivery_date(self):
        delivery_date = self.cleaned_data.get("delivery_date")
        time_now = timezone.now().date()
        if delivery_date < time_now:
            raise forms.ValidationError('You can"t make make a time lesser than today')
        return  delivery_date


class OrderForm2(forms.ModelForm):
    class Meta:
        model =  Order
        fields = ('quantity', 'amount', 'paid', 'delivery_date', 'description')
        widgets = {
            'delivery_date' : forms.DateInput(attrs = {"type":"date"})
        }

    def clean_paid(self):
        paid = self.cleaned_data.get("paid")
        amount = self.cleaned_data.get("amount")
        if paid > amount:
            raise forms.ValidationError('You can"t paid more than the initial amount')
        return  paid


    def clean_delivery_date(self):
        delivery_date = self.cleaned_data.get("delivery_date")
        time_now = timezone.now().date()
        if delivery_date < time_now:
            raise forms.ValidationError('You can"t make make a time lesser than today')
        return  delivery_date

class MeasurementForm(forms.ModelForm):
    class Meta:
        model =  Measurement
        fields = ('customer',
            "neck",
                "waist",
                "wrist",
                "sleeve_length",
                "chest",
                'shoulder',
                'thigh',
                'ankle')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(tailor = self.request.user)

class MeasurementForm2(forms.ModelForm):
    class Meta:
        model =  Measurement
        fields = ("neck",
                "waist",
                "wrist",
                "sleeve_length",
                "chest",
                'shoulder',
                'thigh',
                'ankle')

class ExtraMeasurementForm(forms.ModelForm):
    class Meta:
        model =  ExtraMeasurement
        fields = ( 'name', 'value')
