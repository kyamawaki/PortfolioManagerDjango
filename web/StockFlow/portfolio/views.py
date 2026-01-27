from django.shortcuts import render, redirect, get_object_or_404
from .models import Asset, Transaction, Price, Holding
from .forms import AssetForm, HoldingForm
# import aggregation tools
from django.db.models import Sum, F

# Create your views here.
def asset_list(request):
    # retreve all asset model
    assets = Asset.objects.all()
    # pass the assets when rendering portfolio/asset_list.html
    return render(request, "portfolio/asset_list.html", {"assets": assets})

#################################
# create asset
#################################
def asset_create(request):
    if request.method == "POST":
        # Create a form with registration data
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            # return to asset_list view
            return redirect("asset_list")
    else:
        # Create empty form
        form = AssetForm()
        return render(request, "portfolio/asset_form.html", {"form": form})

def asset_edit(request, pk):
    # If no model matches the pk, raise a 404 error.
    # The model automatically creates a primary key (=id)
    asset = get_object_or_404(Asset, pk=pk)

    if request.method == "POST":
        # request.POST is user sending data
        # instance is asset that exists
        form = AssetForm(request.POST, instance=asset)
        if form .is_valid():
            # update model in DB
            form.save()
            return redirect("asset_list")
    else:
        form = AssetForm(instance=asset)

    # show html with form
    return render(request, "portfolio/asset_form.html", {"form": form})

def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk)

    if request.method == "POST":
        asset.delete()
        return redirect("asset_list")

    return render(request, "portfolio/asset_confirm_delete.html", {"asset": asset})


#################################
# list portfolio
#################################
def portfolio_list(request):
    # collect transaction's simbol (distinct eliminates duplicates)
    # SQL statement : SELECT DISTINCT symbol FROM transactions;
    symbols = Transaction.objects.values_list('symbol', flat=True).distinct()
    portfolios = []

    for symbol in symbols:
        # Take out buy and sell transactions
        # SQL statemnet: SELECT symbol FROM transactions WHERE symbol='ticker' AND type='BUY';
        buys = Transaction.objects.filter(symbol=symbol, type='BUY')
        sells = Transaction.objects.filter(symbol=symbol, type='SELL')

        # Calculate the total amount of buys and purchase amount
        # you can write scripts below
        # result = buys.aggregate(sum_val=Sum('quantity'))
        # total_by_qty = result['sum_val'] (eg. result={'sum_val', 100})
        total_buy_qty = buys.aggregate(total=Sum('quantity'))['total'] or 0
        # F() refers directly to the databes fields
        total_buy_cost = buys.aggregate(total=Sum('quantity') * F('price'))['total'] or 0
        total_sell_qty = sells.aggregate(total=Sum('quantity'))['total'] or 0
        current_qty = total_buy_qty - total_sell_qty

        average_buy_price = total_buy_cost / total_buy_qty if total_buy_qty > 0 else 0

        # latest price
        latest_price = Price.objects.filter(symbol=symbol).order_by('-date').first()
        current_price = latest_price.close if latest_price else None

        # profit
        profit_loss = None
        if current_price is not None:
            profit_loss = (current_price - average_buy_price) * current_qty

        portfolios.append({
            'symbol': symbol,
            'average_buy_price': average_buy_price,
            'current_price': current_price,
            'current_qty': current_qty,
            'profit_loss': profit_loss,
            })

        # send portfolios to html
        return render(request, 'portfolio/portfolio_list.html', {'portfolios': portfolios})


#################################
# list holdings
#################################
def holding_list(request):
    holdings = Holding.objects.all()
    return render(request, 'portfolio/holding_list.html', {'holdings': holdings})

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

