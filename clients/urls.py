from django.urls import path

from . import views


urlpatterns = [   
    path('credito/', views.get_credit, name='credit'),   

    path('solicitar-crédito/', views.request_credit, name='request_credit'),
]