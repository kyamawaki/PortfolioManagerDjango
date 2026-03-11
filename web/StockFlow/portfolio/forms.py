import re
from django import forms
from .models import Asset
import yfinance as yf

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["name", "asset_class", "owner", "financial_institution", "account_type", "ticker", "quantity", "average_price_usd", "average_price_jpy"]

    # インスタンス初期化
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # フィールドの検証
    def clean(self):
        asset_class = self.cleaned_data.get('asset_class')
        ticker = self.cleaned_data.get('ticker')

        # Ticker存在チェック
        if asset_class == "US_STOCK":
            self.validate_us_stock(ticker)
        elif asset_class == 'JP_STOCK':
            self.validate_jp_stock(ticker)
        elif asset_class == "JP_FUND":
            self.validate_jp_fund(ticker)

        # アセットに応じたフィールド値の設定
        if asset_class == 'US_STOCK':
            self.cleaned_data['average_price_jpy'] = None
        elif asset_class == 'US_BND':
            self.cleaned_data['account_type'] = None
            self.cleaned_data['average_price_jpy'] = None
        elif asset_class == 'US_MMF':
            self.cleaned_data['account_type'] = None
            self.cleaned_data['average_price_usd'] = None
            self.cleaned_data['average_price_jpy'] = None
        elif asset_class == 'US_CASH':
            self.cleaned_data['account_type'] = None
            self.cleaned_data['average_price_usd'] = None
            self.cleaned_data['average_price_jpy'] = None
        elif asset_class == 'JP_STOCK':
            self.cleaned_data['average_price_usd'] = None
        elif asset_class == 'JP_FUND':
            self.cleaned_data['average_price_usd'] = None
        elif asset_class == 'JP_BND':
            self.cleaned_data['account_type'] = None
            self.cleaned_data['average_price_usd'] = None
            self.cleaned_data['average_price_jpy'] = None
        elif asset_class == 'JP_CASH':
            self.cleaned_data['account_type'] = None
            self.cleaned_data['average_price_usd'] = None
            self.cleaned_data['average_price_jpy'] = None

    # ticker確認
    def validate_us_stock(self, ticker):
        try:
            data = yf.Ticker(ticker).history(period="1d")
        except Exception:
            raise forms.ValidationError("ティッカー確認中にエラーが発生しました。時間をおいて確認してください")

        if data.empty:
            raise forms.ValidationError("このティッカーは存在しません")

    # 証券コード検証
    def validate_jp_stock(self, ticker):
        if not re.match(r'^\d{4}$', ticker):
            raise forms.ValidationError("日本の証券コードは4桁です")

    # 投信協会コード検証
    def validate_jp_fund(self, ticker):
        if not re.match(r'^[a-z0-9]{8,10}$', ticker, re.IGNORECASE):
            raise forms.ValidationError("投信協会コードは8〜10桁以内の英数字です")

