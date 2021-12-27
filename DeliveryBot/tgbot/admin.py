from django.contrib import admin

from .models import TgUser, FoodType, Food, Order
# Register your models here.


@admin.register(TgUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'chat_id',
        'firstname',
        'username',
        'phone',
        'stage'
    )


@admin.register(FoodType)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'calldata'
    )


@admin.register(Food)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'text',
        'calldata',
        'price'
    )


@admin.register(Order)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'chat_id',
        'type',
        'food',
        'quantity',
        'status'
    )
