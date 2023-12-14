from django.contrib import admin

from shop.models import Product, Order, PaymentLog, UserVault, Coupon, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'paid', 'created', 'updated', 'total_cost', 'discount_value', 'identifier', 'status']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemAdmin]


@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    pass


@admin.register(UserVault)
class UserVaultAdmin(admin.ModelAdmin):
    pass


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass

