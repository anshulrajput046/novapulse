from django.contrib import admin

# Register your models here.


from django.contrib import admin

from apps.arbitrage_scanner.models.arbitrage_opportunity import ArbitrageOpportunity


@admin.register(ArbitrageOpportunity)
class ArbitrageOpportunityAdmin(admin.ModelAdmin):
    list_display = ('id', 'symbol', 'direction', 'binance_price', 'solana_price', 'profit', 'created', 'modified')
    list_display_links = ('id', 'symbol')
    search_fields = ('symbol', 'direction')
    list_filter = ('direction', 'created', 'modified', 'symbol')

    ordering = ('-created',)

    readonly_fields = ('created', 'modified')

    def binance_price_display(self, obj):
        return f"{obj.binance_price:.10f}" if obj.binance_price else None
    binance_price_display.short_description = 'Binance Price'

    def solana_price_display(self, obj):
        return f"{obj.solana_price:.10f}" if obj.solana_price else None
    solana_price_display.short_description = 'Solana Price'

    def profit_display(self, obj):
        return f"{obj.profit:.10f}" if obj.profit else None
    profit_display.short_description = 'Profit'
