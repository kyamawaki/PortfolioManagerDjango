from django.db import models
from decimal import Decimal

################################################
# Holding Model
################################################
class Holding(models.Model):
    name = models.CharField("名前", max_length=100, unique=True)
    ticker = models.CharField("Ticker", max_length=10)
    quantity = models.PositiveIntegerField("数量")
    average_price = models.DecimalField("平均買値（ドル）", max_digits=10, decimal_places=2)
    current_price = models.DecimalField("現在価格（ドル）", max_digits=10, decimal_places=2, null=True, blank=True)
    current_price_jpy = models.DecimalField("現在価格（円）", max_digits=10, decimal_places=2, null=True, blank=True)
    exchange_rate = models.DecimalField("為替レート", max_digits=6, decimal_places=2, default=150.00)
    last_updated = models.DateField(null=True, blank=True)

    # 現在価格（USD）
    @property
    def valuation(self):
        if self.current_price:
            return self.current_price * self.quantity
    
    # 現在価格（日本円）
    @property
    def valuation_jpy(self):
        return self.valuation * self.exchange_rate

    # 評価額（USD）
    @property
    def profit(self):
        if self.current_price:
            return (self.current_price - self.average_price) * self.quantity
        return 0
    
    # 評価額（日本円）
    @property
    def profit_jpy(self):
        return self.profit * self.exchange_rate

    # 資産に対する割合
    @property
    def ratio(self):
        from .models import Holding
        total = sum(h.valuation_jpy for h in Holding.objects.all())
        ratio_value = self.valuation_jpy / total * 100 if total > 0 else 0
        return (Decimal)(ratio_value)

    def __str__(self):
        return f"{self.name} ({self.ticker})"

