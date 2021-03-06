from django.contrib import admin
from models import Currency, ExchangeRate

class CurrencyAdmin(admin.ModelAdmin):
    search_fields = ('code',)
    list_display = ('code', 'name', 'order')


class ExchangeRateAdmin(admin.ModelAdmin):
    search_fields = ('source__code', 'target__code')
    list_display = ('source', 'target', 'rate', 'last_updated_at')
    list_select_related = ('source', 'target')
    raw_id_fields = ('source', 'target')
    readonly_fields = ('last_updated_at', )

    class Meta:
        model = ExchangeRate


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ExchangeRate, ExchangeRateAdmin)
