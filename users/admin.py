from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',   
        'username',
        'email',
        'document_number',
        'mobile_number',
        'is_active',
        'office_name',
        'office_phone_number',
        'company',
        'created_from_server',
    ]
    
    list_filter = [
        'company', 
        'office_name', 
        'created_from_server', 
        'is_active'
    ]

    search_fields = ['first_name', 'username', 'email']


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