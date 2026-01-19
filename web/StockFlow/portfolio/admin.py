from django.contrib import admin
from django.contrib import admin
from .models import Asset, Transaction, Price

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
    list_filter = ('symbol', 'date')
    search_fields = ('symbol',)


