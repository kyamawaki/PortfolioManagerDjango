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

# A decorator to register the Price model in the Django admin site
@admin.register(Price)
# Define the admin configuration class for the Price model
class PriceAdmin(admin.ModelAdmin):
    # Specify the columns to display on the "List Screen" of the admin page
    list_display = ('symbol', 'date', 'close')
    # Added a process called update_price to the "Actions"
    actions = ['update_price']

    # Called when update price is pressed
    # queryset is the set of prices checked by the user.
    def update_price(self, request, queryset):
        symbols = queryset.values_list('symbol',flat = True).distinct()
        for symbol in symbols:
            # call method in services.py
            fetch_latest_price(symbol)
        self.message_user(request, "Update Price")

    # This string will be displayed in the "Action" drop-down on the list screen.
    update_price.short_description = "Update price of selected portfolio"
from django.contrib import admin
from .models import Holding
from .services import fetch_latest_price

#################################################################
@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ('name', 'ticker', 'quantity', 'average_price', 'current_price', 'valuation_display', 'profit_display')
    search_fields = ('name', 'ticker')
    actions = ['update_prices']

    def valuation_display(self, obj):
        return f"{obj.valuation_jpy():,.0f} 円"
    valuation_display.short_description = "評価額（円）"

    def profit_display(self, obj):
        return f"{obj.profit_jpy():,.0f} 円"
    profit_display.short_description = "損益（円）"

    def update_prices(self, request, queryset):
        updated = 0
        for holding in queryset:
            price = fetch_latest_price(holding.ticker)
            if price:
                holding.current_price = price
                holding.save()
                updated += 1
        self.message_user(request, f"{updated} 件の株価を更新しました。")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

