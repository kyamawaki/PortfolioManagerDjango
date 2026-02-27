from django.test import TestCase
from decimal import Decimal
from .models import Asset


class AssetModelTests(TestCase):
    def test_us_mmf_valuation_and_profit(self):
        # USD MMF: current price equals exchange rate
        asset = Asset(
            asset_class="US_MMF",
            quantity=Decimal('100'),
            exchange_rate=Decimal('150'),
            average_price_jpy=Decimal('135'),
        )
        # simulate price update
        asset.current_price_usd = asset.exchange_rate

        # valuation_jpy = qty * rate
        self.assertEqual(asset.valuation_jpy, Decimal('15000'))
        # profit_jpy = (rate - avg_jpy) * qty
        expected_profit = (asset.exchange_rate - asset.average_price_jpy) * asset.quantity
        self.assertEqual(asset.profit_jpy, expected_profit)

    def test_jp_bnd_and_cash_values(self):
        bnd = Asset(asset_class="JP_BND", quantity=Decimal('200'))
        cash = Asset(asset_class="JP_CASH", quantity=Decimal('300'))
        # valuation should equal quantity
        self.assertEqual(bnd.valuation_jpy, Decimal('200'))
        self.assertEqual(cash.valuation_jpy, Decimal('300'))
        # profit = valuation - quantity => 0
        self.assertEqual(bnd.profit_jpy, Decimal('0'))
        self.assertEqual(cash.profit_jpy, Decimal('0'))
