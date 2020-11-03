from django.conf.urls import url
from . import views
from master.views import ConsigneeCreate, ProductCreate, CategoryCreate, SubcategoryCreate, FreightCreate, RouteCreate, FreightforrouteCreate
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

app_name = 'master'

urlpatterns = [
    url(r'productcat', views.CategoryCreate.as_view(), name= 'productcat'),

    url(r'product', views.ProductCreate.as_view(),name='product'),
    # url(r'dashboard', views.dash, name= 'dash'),
    # url(r'userregister', views.register, name= 'reg'),
    url(r'consignee/', views.ConsigneeCreate.as_view(), name= 'consignee'),
    url(r'psubcat', views.SubcategoryCreate.as_view(), name= 'psubcat'),
    url(r'vehicletype', views.VehiceltypeCreate.as_view(), name= 'vtype'),
    url(r'vehicle', views.VehicleCreate.as_view(), name= 'vehicle'),
    url(r'freighttype', views.FreightCreate.as_view(), name= 'ftype'),
    url(r'froute', views.FreightforrouteCreate.as_view(), name= 'froute'),
    url(r'route', views.RouteCreate.as_view(), name= 'route'),
    # url(r'', views.login, name= 'login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)