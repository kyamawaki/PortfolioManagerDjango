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
