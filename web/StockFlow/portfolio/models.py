from django.db import models
from decimal import Decimal

################################################
# Asset Model
################################################
class Asset(models.Model):

    name = models.CharField("名前", max_length=100, unique=True)
    ticker = models.CharField("Ticker", max_length=10)
    quantity = models.DecimalField("数量", max_digits=10, decimal_places=2, default=0)
    average_price_usd = models.DecimalField("平均買値（USD）", max_digits=10, decimal_places=2, null=True, blank=True)
    average_price_jpy = models.DecimalField("平均買値（JPY）", max_digits=10, decimal_places=2, null=True, blank=True)
    current_price_usd = models.DecimalField("現在価格（USD）", max_digits=10, decimal_places=2, null=True, blank=True)
    current_price_jpy = models.DecimalField("現在価格（JPY）", max_digits=10, decimal_places=2, null=True, blank=True)
    exchange_rate = models.DecimalField("為替レート", max_digits=6, decimal_places=2, default=150.00)
    last_updated = models.DateField(null=True, blank=True)

    # 資産クラス
    ASSET_CLASS_CHOICES = [
        ('US_STOCK', '外国株'),
        ('US_BND', '外国債権'),
        ('US_MMF', 'ドル建てMMF'),
        ('US_CASH', 'ドル建て現金'),
        ('JP_STOCK', '日本株'),
        ('JP_FUND', '投資信託'),
        ('JP_BND', '国内債券'),
        ('JP_CASH', '現金'),
    ]
    asset_class = models.CharField(
        max_length=20,
        choices=ASSET_CLASS_CHOICES,
        default='JP_FUND',
    )

    # 所有者
    owner = models.CharField("所有者", max_length=100, null=True, blank=True)

    # 金融機関名
    financial_institution = models.CharField("金融機関名", max_length=100, null=True, blank=True)

    # 口座種別
    ACCOUNT_TYPE_CHOICES = [
        ('TAXABLE', '特定'),
        ('NISA', 'NISA'),
    ]
    account_type = models.CharField(
        "口座種別",
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        null=True,
        blank=True,
    )

    # 資産クラスごとの必須入力と固定ticker定義
    REQUIRED_FIELDS_BY_CLASS = {
        'US_STOCK': ['ticker', 'average_price_usd'],
        'US_BND'  : ['ticker', 'average_price_jpy'],
        'US_MMF'  : ['average_price_jpy'],
        'US_CASH' : [],
        'JP_STOCK': ['ticker', 'average_price_jpy'],
        'JP_FUND' : ['ticker', 'average_price_jpy'],
        'JP_BND'  : [],
        'JP_CASH' : [],
    }

    FIXED_TICKER = {
        'US_BND' : 'US_BND',
        'US_MMF' : 'US_MMF',
        'US_CASH': 'US_CASH',
        'JP_BND' : 'JP_BND',
        'JP_CASH': 'JP_CASH',
    }

    @classmethod
    def required_fields(cls, asset_class):
        return cls.REQUIRED_FIELDS_BY_CLASS.get(asset_class, [])

    @classmethod
    def fixed_ticker(cls, asset_class):
        return cls.FIXED_TICKER.get(asset_class)

    # 海外資産判定
    @property
    def is_foreign_asset(self):
        # treat any US denominated asset as foreign
        return self.asset_class in ("US_STOCK", "US_BND", "US_MMF", "US_CASH")

    # 海外株判定
    @property
    def is_usstock_asset(self):
        return self.asset_class == "US_STOCK"

    # 海外債権判定
    @property
    def is_usbnd_asset(self):
        return self.asset_class == "US_BND"

    # ドル建てMMF判定
    @property
    def is_usmmf_asset(self):
        return self.asset_class == "US_MMF"

    # ドル建て現金判定
    @property
    def is_uscash_asset(self):
        return self.asset_class == "US_CASH"

    # 日本株判定
    @property
    def is_jpstock_asset(self):
        return self.asset_class in ("JP_STOCK",)

    # 投資信託判定
    @property
    def is_jpfund_asset(self):
        return self.asset_class in ("JP_FUND",)

    # 国内債券判定
    @property
    def is_jpbnd_asset(self):
        return self.asset_class in ("JP_BND",)

    # 評価額（USD）
    @property
    def valuation_usd(self):
        if self.current_price_usd is None:
            return Decimal('0')
        # 株式は一株あたりの価格x数量
        if self.is_usstock_asset:
            return self.current_price_usd * self.quantity
        # ドル建て債権は current_price_usd を返す（fetch_latest_price_usbnd が数量を返す）
        elif self.is_usbnd_asset:
            return self.current_price_usd
        # 外貨建てMMF/外貨のUSD評価は数量そのもの（単位: USD）
        elif self.is_usmmf_asset or self.is_uscash_asset:
            return self.quantity
        return Decimal('0')
    
    # 評価額（JPY）
    @property
    def valuation_jpy(self):
        # print(f"{self.ticker}, {self.asset_class}")
        # print(f"{self.current_price_jpy}, {self.quantity}")

        # 米国株/ドル建て債権
        if self.is_usstock_asset or self.is_usbnd_asset:
            value = self.valuation_usd * self.exchange_rate
            return value
        # ドル建てMMF/ドル建て現金
        elif self.is_usmmf_asset or self.is_uscash_asset:
            value = self.valuation_usd * self.exchange_rate
            return value
        # 日本株
        elif self.is_jpstock_asset:
            if self.current_price_jpy and self.quantity:
                value = self.current_price_jpy * self.quantity
                return value
        # 投資信託
        elif self.is_jpfund_asset:
            if self.current_price_jpy and self.quantity:
                value = self.current_price_jpy * self.quantity / 10000
                return value
        # 国内債券は数量と同じ
        elif self.is_jpbnd_asset:
            return self.quantity
        # 国内現金も数量と同じ
        elif self.asset_class == 'JP_CASH':
            return self.quantity
        
        return Decimal('0')
  
    # 損益（USD）
    @property
    def profit_usd(self):
        #print(f"{self.ticker}, {self.asset_class}")
        # 外国株
        if self.is_usstock_asset:
            if self.current_price_usd and self.average_price_usd:
                return (self.current_price_usd - self.average_price_usd) * self.quantity
        # ドル建て債権    
        elif self.is_usbnd_asset:
            if self.average_price_usd:
                return (self.current_price_usd - self.average_price_usd)
        # US_MMF/US_CASHの評価額は現地価格では0
        elif self.is_usmmf_asset or self.is_uscash_asset:
            return Decimal('0')

        # その他JPY資産はUSD損益なし
        return Decimal('0')

    # 損益（JPY）
    @property
    def profit_jpy(self):
        # 米国株(USD損益×為替レート)
        if self.is_usstock_asset:
            return self.profit_usd * self.exchange_rate
        # ドル建て債権(JPY評価額－JPY買値)
        elif self.is_usbnd_asset:
            if self.valuation_jpy and self.average_price_jpy:
                return self.valuation_jpy - self.average_price_jpy
        # 外貨建てMMFは（為替レートの差x数値）
        elif self.is_usmmf_asset:
            if self.average_price_jpy and self.exchange_rate:
                profit = (self.exchange_rate - self.average_price_jpy) * self.quantity
                return profit
        # 外貨現金は買値がわからないので損益はなし
        elif self.is_uscash_asset:
            return Decimal('0')
        # その他JPY資産
        else:
            profit = Decimal('0')
            if self.current_price_jpy and self.average_price_jpy:
                profit = (self.current_price_jpy - self.average_price_jpy) * self.quantity
            if self.is_jpfund_asset:
                return profit / Decimal('10000')
            return profit

    # 資産に対する割合
    @property
    def ratio(self):
        from .models import Asset
        total = sum(asset.valuation_jpy for asset in Asset.objects.all())
        if total > 0:
            ratio_value = self.valuation_jpy / total * 100 if total > 0 else 0
            return (Decimal)(ratio_value)
        else:
            return Decimal('0')

    def __str__(self):
        return f"{self.name} ({self.ticker})"

