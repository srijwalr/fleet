from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from app import views

admin.autodiscover()
urlpatterns = [
    path('admin/', admin.site.urls),
    url('', include('app.urls')),
    # url('accounts/', include('accounts.urls')),
    # url('master/', include('master.urls')),
    # url('fleet/', include('app.urls')),
	# path('jet_api/', include('jet_django.urls')),
    url(r'^driver-autocomp/$', views.DriverAutocomp.as_view(), name='driver-autocomp'),
    url(r'^veh-autocomp/$', views.VehAutocomp.as_view(), name='veh-autocomp'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += (url(r"^select2/", include("django_select2.urls")), )  