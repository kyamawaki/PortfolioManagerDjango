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

    # 日本株判定
    @property
    def is_jpstock_asset(self):
        return self.asset_class in ("JP_STOCK",)

    # 投資信託判定
    @property
    def is_jpfund_asset(self):
        return self.asset_class in ("JP_FUND",)

    # 現在価格（USD）
    @property
    def valuation_usd(self):
        if self.is_foreign_asset and self.current_price_usd:
            return self.current_price_usd * self.quantity
        return Decimal('0')
    
    # 現在価格（日本円）
    @property
    def valuation_jpy(self):
        # print(f"{self.ticker}, {self.asset_class}")
        # print(f"{self.current_price_jpy}, {self.quantity}")
        if self.is_foreign_asset:
            if self.current_price_usd and self.quantity and self.exchange_rate:
                value = self.current_price_usd * self.quantity * self.exchange_rate
                return value
        else:
            if self.current_price_jpy and self.quantity:
                value = self.current_price_jpy * self.quantity
                if self.is_jpfund_asset:
                    value /= 10000
                return value
            
        return Decimal('0')
  
    # 評価額（USD）
    @property
    def profit_usd(self):
        if self.is_foreign_asset and self.current_price_usd and self.average_price_usd:
            profit = (self.current_price_usd - self.average_price_usd) * self.quantity
            return profit
        return 0
    
    # 評価額（日本円）
    @property
    def profit_jpy(self):
        if self.is_foreign_asset:
            return self.profit_usd * self.exchange_rate
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

