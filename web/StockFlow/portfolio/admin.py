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

