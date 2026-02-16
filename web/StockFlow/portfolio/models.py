from django.db import models
from decimal import Decimal

################################################
# Asset Model
################################################
class Asset(models.Model):

    ticker = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField("名前", max_length=100, unique=True)
    ticker = models.CharField("Ticker", max_length=10)
    quantity = models.PositiveIntegerField("数量")
    average_price = models.DecimalField("平均買値（ドル）", max_digits=10, decimal_places=2)
    current_price = models.DecimalField("現在価格（ドル）", max_digits=10, decimal_places=2, null=True, blank=True)
    current_price_jpy = models.DecimalField("現在価格（円）", max_digits=10, decimal_places=2, null=True, blank=True)
    exchange_rate = models.DecimalField("為替レート", max_digits=6, decimal_places=2, default=150.00)
    last_updated = models.DateField(null=True, blank=True)

    # 資産クラス
    ASSET_CLASS_CHOICES = [
        ('JP_STOCK', '日本株'),
        ('US_STOCK', '海外株'),
        ('REAL_ESTATE', '不動産'),
        ('GOLD', '貴金属'),
        ('JP_BOND', '国内債券'),
        ('US_BOND', '海外債権'),
        ('CASH', '現金'),
    ]
    asset_class = models.CharField(
        max_length=20,
        choices=ASSET_CLASS_CHOICES,
        default='JP_STOCK',
    )

    # 海外資産判定
    def is_foreign_asset(self):
        return self.asset_class in ("US_STOCK", "US_BOND")

    # 現在価格（USD）
    @property
    def valuation(self):
        if self.current_price is not None:
            return self.current_price * self.quantity
        return Decimal('0')
    
    # 現在価格（日本円）
    @property
    def valuation_jpy(self):
        if self.is_foreign_asset:
            return self.valuation * self.exchange_rate
        else:
            return self.valuation

    # 評価額（USD）
    @property
    def profit(self):
        if self.current_price:
            return (self.current_price - self.average_price) * self.quantity
        return 0
    
    # 評価額（日本円）
    @property
    def profit_jpy(self):
        if self.is_foreign_asset:
            return self.profit * self.exchange_rate
        else:
            return self.profit

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

