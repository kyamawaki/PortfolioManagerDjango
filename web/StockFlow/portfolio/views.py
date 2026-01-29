from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
from .models import Holding
from .forms import HoldingForm

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

