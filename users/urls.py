from django.urls import path
from django.contrib.auth import views as auth_views
from app import settings

from . import views


urlpatterns = [   
    path('', views.custom_login, name='login'),
    
    path('email-login/', views.email_login, name='email_login'),

    path('codigo-referido/', views.reffered_code_view, name='reffered_code'), 

    path(
        'nuevo-cliente/<str:referred_code>/<str:company_id>/<str:office_name>/<str:office_phone_number>/', 
        views.create_user_view, 
        name='create_user'
    ), 

    path(
        'logout/', 
        auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), 
        name='logout'
    ),
]