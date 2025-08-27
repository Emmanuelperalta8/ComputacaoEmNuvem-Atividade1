from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def home(request):
    return HttpResponse("Django está rodando no Docker! 🚀")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),  # Adiciona a rota para "/"
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)