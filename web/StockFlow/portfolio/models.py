from django.db import models

# Create your models here.
class Asset(models.Model):
    ASSET_CLASS_CHOICES = [
            ("stock", "Stock"),
            ("bond", "Bond"),
            ("reit", "REIT"),
            ("commodity", "Comodity"),
            ("cash", "Cash"),
        ]

    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=20, unique=True)
    asset_class = models.CharField(max_length=20, choices=ASSET_CLASS_CHOICES)
    currency = models.CharField(max_length=10, default="USD")

    def __str__(self):
        return f"{selft.ticker} - {self.name}"

################################################
class Transaction(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'
    TYPE_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    symbol = models.CharField(max_length=20)
    date = models.DateField()
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    price = models.DecimalField(max_digits=12, decimal_places=4)
    type = models.CharField(max_length=4, choices=TYPE_CHOICES)

    @property
    def amount(self):
        return self.quantity * self.price

################################################
class Price(models.Model):
    symbol = models.CharField(max_length=20)
    date = models.DateField()
    close = models.DecimalField(max_digits=12, decimal_places=4)

################################################
from django.db import models

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

