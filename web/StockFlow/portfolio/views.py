from django.shortcuts import render, redirect, get_object_or_404
from .models import Asset
from .forms import AssetForm

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

