from django import forms
from .models import Order


class DateInput(forms.DateInput):
    input_type = 'date'



class OrderModelFormForAdmin(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'book', 'end_at']
        labels = {
            'user': 'Select user',
            'book': 'Select book',
            'end_at': 'Date to end subscribe',
        }
        widgets = {
            'end_at' : DateInput
        }
class OrderModelFormForUser(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['book', 'end_at']
        labels = {
            # 'user': 'Select user',
            'book': 'Select book',
            'end_at': 'Date to end subscribe',
        }
        widgets = {
            'end_at' : DateInput
        }


class DeleteOrderUser(forms.Form):
    orders = forms.IntegerField(required=True,
                                label="Choose order id:")


class DeleteOrderAdmin(forms.Form):

    orders = forms.ModelChoiceField(Order.objects.all(),
                                       required=True,
                                       label="Choose order:")


class UpdateOrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['book', 'plated_end_at']
        labels = {
            'book': 'Select book',
            'plated_end_at': 'Date to end subscribe',
        }
        widgets = {
            'plated_end_at' : DateInput
        }
