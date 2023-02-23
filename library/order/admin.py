from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'plated_end_at', 'end_at', 'created_at')
    # fields = ('book', 'user', ('plated_end_at', 'end_at'))
    list_filter = ('book', 'user', 'plated_end_at', 'end_at', 'created_at')
    fieldsets = (

        (None,{
            'fields': ('book', 'user', 'created_at')
        }),
        ('Date to end',{
            'classes': ('collapse',),
            'fields': (('end_at', 'plated_end_at'),)
        }),

    )
    date_hierarchy = 'plated_end_at'
    empty_value_display = '-empty-'
    readonly_fields = ('created_at',)

# pass

# admin.site.register(Order, OrderAdmin)