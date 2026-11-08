
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.http import HttpResponse


def health_check(request):
    return HttpResponse("OK", content_type="text/plain")


urlpatterns = [
    path('healthz/', health_check, name='health_check'),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('documents/', include('documents.urls')),
    path('audit/', include('audit.urls')),
]
