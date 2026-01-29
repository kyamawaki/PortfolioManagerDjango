from django.db import models

################################################
# Holding Model
################################################
class Holding(models.Model):
    name = models.CharField("名前", max_length=100, unique=True)
    ticker = models.CharField("Ticker", max_length=10)
    quantity = models.PositiveIntegerField("数量")
    average_price = models.DecimalField("平均買値（ドル）", max_digits=10, decimal_places=2)
    current_price = models.DecimalField("現在価格（ドル）", max_digits=10, decimal_places=2, null=True, blank=True)
    exchange_rate = models.DecimalField("為替レート", max_digits=6, decimal_places=2, default=150.00)

    # 現在価格（日本円）
    def valuation_jpy(self):
        if self.current_price:
            return self.current_price * self.quantity * self.exchange_rate
        return 0

    # 評価額（日本円）
    def profit_jpy(self):
        if self.current_price:
            return (self.current_price - self.average_price) * self.quantity * self.exchange_rate
        return 0

    def __str__(self):
        return f"{self.name} ({self.ticker})"

