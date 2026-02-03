from django import forms
from .models import Holding
import yfinance as yf

class HoldingForm(forms.ModelForm):
    class Meta:
        model = Holding
        fields = ["name", "ticker", "quantity", "average_price"]

    def clean_ticker(self):
        ticker = self.cleaned_data['ticker']

        # 存在チェック
        try:
            data = yf.Ticker(ticker).history(period="1d")
        except Exception:
            raise forms.ValidationError("ティッカー確認中にエラーが発生しました。時間をおいて確認してください")

        if data.empty:
            raise forms.ValidationError("このティッカーは存在しません")

        return ticker
