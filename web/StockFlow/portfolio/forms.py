from django import forms
from .models import Asset, Holding

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["name", "ticker", "asset_class", "currency"]

class HoldingForm(forms.ModelForm):
    class Meta:
        model = Holding
        fields = ["name", "ticker", "quantity", "average_price"]
