import re
from django import forms
from .models import Asset
import yfinance as yf

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["name", "ticker", "asset_class", "quantity", "average_price"]

    # フィールドの検証
    def clean(self):
        asset_class = self.cleaned_data.get('asset_class')
        ticker = self.cleaned_data.get('ticker')

        # 存在チェック
        if asset_class == 'JP_STOCK':
            self._validate_jp_stock(ticker)
        elif asset_class == "JP_FUND":
            self._validate_jp_fund(ticker)
        elif asset_class == "US_STOCK":
            self._validate_us_stock(ticker)

    # 証券コード検証
    def _validate_jp_stock(self, ticker):
        if not re.match(r'^\d{4}$', ticker):
            raise forms.ValidationError("日本の証券コードは4桁です")

    # 投信協会コード検証
    def _validate_jp_fund(self, ticker):
        if not re.match(r'^[a-z0-9]{8,10}$', ticker, re.IGNORECASE):
            raise forms.ValidationError("投信協会コードは8〜10桁以内の英数字です")

    # ticker確認
    def _validate_us_stock(self, ticker):
        try:
            data = yf.Ticker(ticker).history(period="1d")
        except Exception:
            raise forms.ValidationError("ティッカー確認中にエラーが発生しました。時間をおいて確認してください")

        if data.empty:
            raise forms.ValidationError("このティッカーは存在しません")
