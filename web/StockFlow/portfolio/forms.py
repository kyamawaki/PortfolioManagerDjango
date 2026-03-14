import re
from django import forms
from .models import Asset
from django.core.exceptions import ValidationError
import yfinance as yf

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["name", "asset_class", "owner", "financial_institution", "account_type", "ticker", "quantity", "average_price_usd", "average_price_jpy", "average_exchange_rate"]

    # インスタンス初期化
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        asset_class = cleaned.get('asset_class')
        ticker = cleaned.get('ticker')

        FIXED_TICKERS = {
            'US_BND' : 'US_BND',
            'US_MMF' : 'US_MMF',
            'US_CASH': 'US_CASH',
            'JP_BND' : 'JP_BND',
            'JP_CASH': 'JP_CASH',
        }

        if asset_class in FIXED_TICKERS:
            ticker = FIXED_TICKERS[asset_class]
            cleaned['ticker'] = ticker

        # --- 1. Ticker バリデーションのディスパッチ ---
        validators = {
            "US_STOCK": self.validate_us_stock,
            "JP_STOCK": self.validate_jp_stock,
            "JP_FUND":  self.validate_jp_fund,
        }
        if asset_class in validators:
            validators[asset_class](ticker)

        # --- 2. アセットクラスごとのフィールドクリア設定 ---
        clear_rules = {
            'US_STOCK': ['average_price_jpy'],
            'US_BND':   ['account_type', 'average_price_jpy'],
            'US_MMF':   ['account_type', 'average_price_usd', 'average_price_jpy'],
            'US_CASH':  ['account_type', 'average_price_usd', 'average_price_jpy'],
            'JP_STOCK': ['average_price_usd'],
            'JP_FUND':  ['average_price_usd'],
            'JP_BND':   ['account_type', 'average_price_usd', 'average_price_jpy'],
            'JP_CASH':  ['account_type', 'average_price_usd', 'average_price_jpy'],
        }

        for field in clear_rules.get(asset_class, []):
            cleaned[field] = None

        # --- 3. 新規作成時のみ重複チェック ---
        if self.instance.pk is None:
            name = cleaned.get('name')
            owner = cleaned.get('owner')
            financial_institution = cleaned.get('financial_institution')
            account_type = cleaned.get('account_type')

            print(f"name={name}, \
                owner={owner}, \
                financial_institution={financial_institution}, \
                account_type={account_type},\
                ticker={ticker}")
    
            if Asset.objects.filter(
                name=name,
                owner=owner,
                financial_institution=financial_institution,
                account_type=account_type,
                ticker=ticker
            ).exists():
                raise ValidationError("同じ資産がすでに登録されています")

        print(cleaned)
        return cleaned

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

