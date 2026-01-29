from django import forms
from .models import Holding

class HoldingForm(forms.ModelForm):
    class Meta:
        model = Holding
        fields = ["name", "ticker", "quantity", "average_price"]
