from django.contrib import admin
from django.contrib import admin
from .models import Asset, Transaction, Price
from .services import fetch_latest_price

# Register your models here.
admin.site.register(Asset)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'date', 'type', 'quantity', 'price')
    list_filter = ('symbol', 'type', 'date')
    search_fields = ('symbol',)

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'date', 'close')
    actions = ['update_price']

    def update_price(self, request, queryset):
        symbols = queryset.values_list('symbol',flat = True).distinct()
        for symbol in symbols:
            fetch_latest_price(symbol)
        self.message_user(request, "Update Price")

    update_price.short_description = "Update price of selected portfolio"

