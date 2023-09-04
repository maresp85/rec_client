from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',   
        'username',
        'is_active',
        'is_staff',
    ]
    list_filter = ['is_active']

    search_fields = ['first_name', 'username']


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]

    list_filter = ['is_active']

    search_fields = ['name']


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'country',
    ]

    list_filter = ['is_active', 'country']

    search_fields = ['name']


@admin.register(models.Enterprise)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'mobile_phone',
    ]

    list_filter = ['name']

    search_fields = ['name']