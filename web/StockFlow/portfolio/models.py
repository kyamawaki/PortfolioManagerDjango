from django.db import models
from decimal import Decimal

################################################
# Asset Model
################################################
class Asset(models.Model):

    name = models.CharField("名前", max_length=100, unique=True)
    ticker = models.CharField("Ticker", max_length=10)
    quantity = models.PositiveIntegerField("数量")
    average_price_usd = models.DecimalField("平均買値（USD）", max_digits=10, decimal_places=2, null=True, blank=True)
    average_price_jpy = models.DecimalField("平均買値（JPY）", max_digits=10, decimal_places=2, null=True, blank=True)
    current_price_usd = models.DecimalField("現在価格（USD）", max_digits=10, decimal_places=2, null=True, blank=True)
    current_price_jpy = models.DecimalField("現在価格（JPY）", max_digits=10, decimal_places=2, null=True, blank=True)
    exchange_rate = models.DecimalField("為替レート", max_digits=6, decimal_places=2, default=150.00)
    last_updated = models.DateField(null=True, blank=True)

    # 資産クラス
    ASSET_CLASS_CHOICES = [
        ('JP_STOCK', '日本株'),
        ('US_STOCK', '海外株'),
        ('JP_FUND', '投資信託'),
        ('JP_BOND', '国内債券'),
        ('US_BOND', '海外債権'),
        ('CASH', '現金'),
    ]
    asset_class = models.CharField(
        max_length=20,
        choices=ASSET_CLASS_CHOICES,
        default='JP_FUND',
    )

    # 海外資産判定
    @property
    def is_foreign_asset(self):
        return self.asset_class in ("US_STOCK", "US_BOND")

    # 海外株判定
    @property
    def is_usstock_asset(self):
        return self.asset_class in ("US_STOCK", )

    # 海外債権判定
    @property
    def is_usbnd_asset(self):
        return self.asset_class in ("US_BOND", )

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
        return self.asset_class in ("JP_BOND",)

    # 評価額（USD）
    @property
    def valuation_usd(self):
        if self.current_price_usd is None:
            return Decimal('0')
        # 株式は一株あたりの価格x数量
        if self.is_usstock_asset:
            return self.current_price_usd * self.quantity
        # ドル建て債権の評価額は数量と等しい
        elif self.is_usbnd_asset:
            return self.current_price_usd
        return Decimal('0')
    
    # 評価額（JPY）
    @property
    def valuation_jpy(self):
        # print(f"{self.ticker}, {self.asset_class}")
        # print(f"{self.current_price_jpy}, {self.quantity}")

        # 米国株 / ドル建て債権
        if self.is_usstock_asset or self.is_usbnd_asset:
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
            
        return Decimal('0')
  
    # 損益（USD）
    @property
    def profit_usd(self):
        #print(f"{self.ticker}, {self.asset_class}")
        if self.is_usstock_asset:
            if self.current_price_usd and self.average_price_usd:
                profit = (self.current_price_usd - self.average_price_usd) * self.quantity
                return profit
        # ドル建て債権の損益は買値-現在値（現在値は数量と等しい）
        elif self.is_usbnd_asset:
            if self.average_price_usd:
                profit = (self.current_price_usd - self.average_price_usd)
                return profit
        return Decimal('0')
    
    # 損益（JPY）
    @property
    def profit_jpy(self):
        # 米国株(損益*為替レート)
        if self.is_usstock_asset:
            return self.profit_usd * self.exchange_rate
        # ドル建て債権(円建ての買値から計算)
        elif self.is_usbnd_asset:
            # print(f"{self.current_price_jpy}, {self.average_price_jpy}")
            if self.valuation_jpy and self.average_price_jpy:
                profit = (self.valuation_jpy - self.average_price_jpy)
                return profit
        else:
            profit = 0
            if self.current_price_jpy and self.average_price_jpy:
                profit = (self.current_price_jpy - self.average_price_jpy) * self.quantity
            if self.is_jpfund_asset:
                return profit / 10000;
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

