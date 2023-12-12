from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.urls import re_path as url

urlpatterns = [
    path('go_admin/', admin.site.urls),
    path('', include('clients.urls')),
    path('', include('users.urls')),
    url('', include('social_django.urls', namespace='social'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'REC Clientes'
admin.site.site_title = 'REC Clientes'
admin.site.index_title = 'REC Clientes'