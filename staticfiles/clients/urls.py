from django.urls import path

from . import views


urlpatterns = [   
    path('credito/', views.get_credit, name='credit'),   
]