from django.contrib import admin

from shop.models import Product, Order, PaymentLog, UserVault


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    pass

@admin.register(UserVault)
class UserVaultAdmin(admin.ModelAdmin):
    pass

