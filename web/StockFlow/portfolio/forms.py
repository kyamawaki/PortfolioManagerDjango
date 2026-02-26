import re
from django import forms
from .models import Asset
import yfinance as yf

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["name", "asset_class", "owner", "financial_institution", "account_type", "ticker", "quantity", "average_price_usd", "average_price_jpy"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初期値やインスタンスのasset_classが国内債券なら平均買値フィールドを隠す
        asset_class = None
        if 'asset_class' in self.initial:
            asset_class = self.initial['asset_class']
        if self.instance and getattr(self.instance, 'asset_class', None):
            asset_class = self.instance.asset_class

        if asset_class == 'JP_BND':
            # 国内債券の場合はtickerにJGBをセットしておく
            self.initial.setdefault('ticker', 'JGB')
            for fld in ('ticker', 'average_price_usd', 'average_price_jpy'):
                # 非表示にしてrequiredを外す
                self.fields[fld].widget = forms.HiddenInput()
                self.fields[fld].required = False

    # フィールドの検証
    def clean(self):
        asset_class = self.cleaned_data.get('asset_class')
        ticker = self.cleaned_data.get('ticker')

        # 存在チェック
        if asset_class == 'JP_STOCK':
            self.validate_jp_stock(ticker)
        elif asset_class == "JP_FUND":
            self.validate_jp_fund(ticker)
        elif asset_class == "US_STOCK":
            self.validate_us_stock(ticker)
        # 国内債券はtickerをJGBにし、平均買値を入力させない
        if asset_class == 'JP_BND':
            self.cleaned_data['ticker'] = 'JGB'
            self.cleaned_data['average_price_usd'] = None
            self.cleaned_data['average_price_jpy'] = None

    # 証券コード検証
    def validate_jp_stock(self, ticker):
        if not re.match(r'^\d{4}$', ticker):
            raise forms.ValidationError("日本の証券コードは4桁です")

    # 投信協会コード検証
    def validate_jp_fund(self, ticker):
        if not re.match(r'^[a-z0-9]{8,10}$', ticker, re.IGNORECASE):
            raise forms.ValidationError("投信協会コードは8〜10桁以内の英数字です")

    # ticker確認
    def validate_us_stock(self, ticker):
        try:
            data = yf.Ticker(ticker).history(period="1d")
        except Exception:
            raise forms.ValidationError("ティッカー確認中にエラーが発生しました。時間をおいて確認してください")

        if data.empty:
            raise forms.ValidationError("このティッカーは存在しません")
