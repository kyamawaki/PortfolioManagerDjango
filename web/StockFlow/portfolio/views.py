from decimal import Decimal
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
from .models import Holding
from .forms import HoldingForm
from .services import fetch_latest_price, fetch_usd_jpy

#################################
# list holdings
#################################
def holding_list(request):
    holdings = Holding.objects.all()

    today = date.today()
    needs_update = any(h.last_updated != today for h in holdings)
    if needs_update:
        usd_jpy = fetch_usd_jpy()
        for h in holdings:
            # float to decimal
            h.exchange_rate = Decimal(str(usd_jpy))
            price = fetch_latest_price(h.ticker)
            # float to decimal
            h.current_price = Decimal(str(price))

            h.last_updated = today
            h.save()

    last_updated = holdings.first().last_updated if holdings else None

    total_valuation = sum(h.valuation or 0 for h in holdings)
    total_valuation_jpy = sum(h.valuation_jpy or 0 for h in holdings)
    total_profit = sum(h.profit or 0 for h in holdings)
    total_profit_jpy = sum(h.profit_jpy or 0 for h in holdings)

    return render(request, 'portfolio/holding_list.html', {'holdings': holdings,
                                                           'last_updated': last_updated,
                                                           'total_valuation': total_valuation,
                                                           'total_valuation_jpy': total_valuation_jpy,
                                                           'total_profit': total_profit,
                                                           'total_profit_jpy': total_profit_jpy,
                  })

#################################
# Add holding
#################################
def holding_create(request):
    if request.method == 'POST':
        form = HoldingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('holding_list')
    else:
        form = HoldingForm()

    return render(request, 'portfolio/holding_create.html', {'form': form})

#################################
# Edit holding
#################################
def holding_edit(request, pk):
    holding = get_object_or_404(Holding, pk=pk)

    if request.method == 'POST':
        form = HoldingForm(request.POST, instance=holding)
        if form.is_valid():
            form.save()
            return redirect('holding_list')
    else:
        form = HoldingForm(instance=holding)

    return render(request, 'portfolio/holding_edit.html', {'form': form, 'holding': holding})

#################################
# Delete holding
#################################
def holding_delete(request, pk):
    holding = get_object_or_404(Holding, pk=pk)
    holding.delete()
    return redirect('holding_list')

#################################
# Update holding
#################################
def holding_update(request):
    usd_jpy = fetch_usd_jpy()
    if usd_jpy is None:
        return None

    today = date.today()
    holdings = Holding.objects.all()
    for h in holdings:
        price = fetch_latest_price(h.ticker)
        if price:
            h.current_price = Decimal(str(price))
            h.exchange_rate = Decimal(str(usd_jpy))
            h.last_updated = today
            h.save()

    return redirect('holding_list')
