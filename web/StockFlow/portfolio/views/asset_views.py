from decimal import Decimal
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
from portfolio.models import Asset
from portfolio.forms import AssetForm
from portfolio.services import fetch_latest_price, fetch_usd_jpy

#################################
# list assets
#################################
def asset_list(request):
    assets = Asset.objects.all()

    today = date.today()
    needs_update = any(asset.last_updated != today for asset in assets)
    if needs_update:
        usd_jpy = fetch_usd_jpy()
        if usd_jpy is None:
            usd_jpy = 0.0

        for asset in assets:
            # float to decimal
            asset.exchange_rate = Decimal(str(usd_jpy))
            price = fetch_latest_price(asset.asset_class, asset.ticker)
            if price:
                # float to decimal
                asset.current_price = Decimal(str(price))

            asset.last_updated = today
            asset.save()

    last_updated = assets.first().last_updated if assets else None

    total_valuation = sum(asset.valuation or 0 for asset in assets)
    total_valuation_jpy = sum(asset.valuation_jpy or 0 for asset in assets)
    total_profit = sum(asset.profit or 0 for asset in assets)
    total_profit_jpy = sum(asset.profit_jpy or 0 for asset in assets)

    exchange_rate = assets[0].exchange_rate if assets else None

    return render(request, 'portfolio/asset_list.html', {'assets': assets,
                                                           'last_updated': last_updated,
                                                           'total_valuation': total_valuation,
                                                           'total_valuation_jpy': total_valuation_jpy,
                                                           'total_profit': total_profit,
                                                           'total_profit_jpy': total_profit_jpy,
                                                           'exchange_rate': exchange_rate,
                  })

#################################
# Add asset
#################################
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset_list')
    else:
        form = AssetForm()

    return render(request, 'portfolio/asset_create.html', {'form': form})

#################################
# Edit asset
#################################
def asset_edit(request, pk):
    asset = get_object_or_404(Asset, pk=pk)

    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('asset_list')
    else:
        form = AssetForm(instance=asset)

    return render(request, 'portfolio/asset_edit.html', {'form': form, 'asset': asset})

#################################
# Delete asset
#################################
def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    asset.delete()
    return redirect('asset_list')

#################################
# Update asset
#################################
def asset_update(request):
    usd_jpy = fetch_usd_jpy()
    if usd_jpy is None:
        return None

    today = date.today()
    assets = Asset.objects.all()
    for asset in assets:
        price = fetch_latest_price(asset.asset_class, asset.ticker)
        if price:
            asset.current_price = Decimal(str(price))
            asset.exchange_rate = Decimal(str(usd_jpy))
            asset.last_updated = today
            asset.save()

    return redirect('asset_list')


