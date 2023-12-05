from django.contrib import admin
from .models import Profile, Transaction, AddBalance



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'balance', 'created_at')
    search_fields = ('user__username', 'phone')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('sender_phone', 'recipient_phone', 'amount', 'created_at')
    search_fields = ('sender_phone', 'recipient_phone')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


@admin.register(AddBalance)
class AddBalanceAdmin(admin.ModelAdmin):
    list_display = ('phone', 'amount', 'created_at')
    search_fields = ('phone',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


