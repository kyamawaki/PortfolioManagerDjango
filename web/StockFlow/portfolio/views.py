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

    return render(request, 'portfolio/holding_list.html', {'holdings': holdings, 'last_updated': last_updated})

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

