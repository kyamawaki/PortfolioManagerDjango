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

