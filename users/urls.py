from django.urls import path

from . import views


urlpatterns = [   
    path('', views.custom_login, name='login'),   

    path('codigo-referido/', views.reffered_code_view, name='reffered_code'), 

    path('nuevo-cliente/<str:referred_code>/<str:company_id>/', views.create_user_view, name='create_user'), 
]