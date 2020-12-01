from django.conf.urls import url
from . import views
from django.urls import path, include
from app.views import DriverAutocomp, VehAutocomp
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
# from rest_framework import routers 
from .views import *
  
# define the router 
# router = routers.DefaultRouter() 
  
app_name = 'app'

# define the router path and viewset to be used 
# router.register(r'trip', TripsheetViewSet) 
# router.register(r'driver', DriverViewSet) 


urlpatterns = [
    url(r'signin',views.sign_in, name= 'signin'),
    url(r'signout', views.LogoutView.as_view(), name = 'signout'),
    url(r'^$', views.FleetView.as_view(), name='fleet'),
    url(r'driver/list/', views.DriverList.as_view(), name='driver-list'),
    # url(r'salary/', views.Salaryreport.as_view(), name = 'salary'),
    url(r'^export/xls/$', views.salary, name='export'),
    url(r'loglist/', views.FuelLogView.as_view(), name='logs'),
    url(r'tripgen/', views.Tripgen, name='tripgen'),
    url(r'detail1/', views.detail, name='detail'),
    url(r'logresult/', views.loglist, name='logresult'),
    url(r'insurance/', views.InsView.as_view(), name='insurance'),
    url(r'tax/', views.TaxView.as_view(), name='tax'),
    url(r'permit/', views.PermitView.as_view(), name='permit'),
    url(r'fitness/', views.FitnessView.as_view(), name='fitness'),
    url(r'pollution/', views.PollutionView.as_view(), name='pollution'),
    url(r'welfare/', views.WelfareView.as_view(), name='welfare'),
    url(r'triplog/', views.TripsheetList.as_view(), name='triplog'),
    url(r'triplist/', views.TripList.as_view(), name='trip-list'),
    url(r'gettrip/', gettrip, name='gettrip'),
    url(r'entry/', entry, name='entry'),
    url(r'list/', views.fleetlist, name='fleet-list'),
    url(r'driverdetail/(?P<pk>[0-9]+)/$', views.DriverDetailView.as_view(), name='driver-detail'),
    url(r'detail/(?P<pk>[0-9]+)/$', views.FleetDetailView.as_view(), name='fleet-detail'),
    url(r'fleet/add/$', views.FleetCreate.as_view(), name='fleet-add'),
    url(r'tripsheet/add/$', views.TripsheetCreate.as_view(), name='tripsheet'),
    # url(r'trip/add/$', views.TripCreate.as_view(), name='trip'),
    url(r'fleet/(?P<pk>[0-9]+)/$', views.FleetUpdate.as_view(), name='fleet-update'),
    url(r'^trips/(?P<filter_by>[a-zA_Z]+)/$', views.trips, name='list'),    
    url(r'trip/(?P<pk>[0-9]+)/$', views.TripUpdate.as_view(), name='trip-update'),
    url(r'fleet/(?P<pk>[0-9]+)/delete/$', views.FleetDelete.as_view(), name='fleet-delete'),
    url(r'fuel-log', views.FuelLogAdd.as_view(),name= 'fuel-log'),
    url(r'log/(?P<pk>[0-9]+)/$', views.LogDetailView.as_view(), name='log-detail'),
    url(r'allocate/(?P<pk>[0-9]+)/$', views.DriverAllocate.as_view(), name = 'allocate'),
    url(r'region/(?P<region_id>[0-9]+)/$',views.region_data, name = 'region'),
    url(r'driver/(?P<pk>[0-9]+)/$', views.DriverUpdate.as_view(), name='driver-update'),
    url(r'expense/(?P<pk>[0-9]+)/$', views.DriverExpense.as_view(), name='expense-update'),
    url(r'pdriver/add/$', views.PDriverCreate.as_view(), name='pdriver'),
    url(r'tdriver/add/$', views.TDriverCreate.as_view(), name='tdriver'),
    # url(r'driver/add/$', views.DriverCreate.as_view(), name='driver')
    # url(r'emi/add/$', views.EmiCreate.as_view(), name='emi-add'),
    # path('api', include(router.urls)), 
    # path('api-auth/', include('rest_framework.urls')) 

    ]