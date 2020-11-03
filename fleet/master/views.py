from django.shortcuts import render
from master.forms import CosingneemasterForm , ProductmasterForm
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView
from django.urls import reverse_lazy
from master.models import Productmaster, Cosingneemaster, Productcategory, Productsubcategory, Freighttypes, Routemaster, Freightforroute, Vehiclemaster, Vehiclecategory


class ConsigneeCreate(CreateView):
    # import pdb; pdb.set_trace()
    model  = Cosingneemaster
    template_name = 'master/consignee.html'
    # form_class = CosingneemasterForm
    success_url = reverse_lazy('app:dash')
    fields = ('consgnem_code','consgnem_name','consgnem_address','consgnem_routtyp','consgnem_district','consgnem_city','consgnem_pincode','consgnem_distance','consgnem_gsttin','consgnem_pan','consgnem_active') 

    #def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        # context["vehicle_types"] =  
        # import pdb;pdb.set_trace()
        #return context

class ProductCreate(CreateView):
    model = Productmaster
    template_name = 'master/product_form.html'
    success_url = reverse_lazy('app:dash')
    fields = ('promas_code','promas_desc','promas_quantity','promas_procat_pntr','promas_proscat_pntr','promas_slno','promas_active','promas_remarks')

class CategoryCreate(CreateView):
    model = Productcategory
    template_name = 'master/productcategory.html'
    success_url = reverse_lazy('app:dash')
    fields = ('procat_code','procat_desc','procat_slno','procat_active','procat_remarks')


class SubcategoryCreate(CreateView):
    model = Productsubcategory
    template_name = 'master/productsubcategory.html'
    success_url = reverse_lazy('app:dash')
    fields =('proscat_code','proscat_procatpntr','proscat_desc','proscat_volume','proscat_weight','proscat_width','proscat_length','proscat_slno','proscat_active','proscat_remarks')

class VehicleCreate(CreateView):
    model = Vehiclemaster
    template_name = 'master/vehicle.html'
    success_url = reverse_lazy('app:dash')
    fields =('vehmas_code','vehmas_frtyppntr','vehmas_catpntr','vehmas_drivername','vehmas_phone','vehmas_desc','vehmas_active')

class VehiceltypeCreate(CreateView):
    model = Vehiclecategory 
    template_name = 'master/vehicletype.html'
    success_url = reverse_lazy('app:dash')
    fields = ('vehcat_code','vehcat_desc','vehcat_wtcapacity','vehcat_length','vehcat_width','vehcat_slno','vehcat_remarks')


class FreightCreate(CreateView):
    model = Freighttypes
    template_name = 'master/freighttype.html'
    success_url = reverse_lazy('app:dash')
    fields = ('fretype_code','fretype_desc','fretype_slno','fretype_remarks','fretype_active')

class RouteCreate(CreateView):
    model = Routemaster
    template_name = 'master/route.html'
    success_url = reverse_lazy('app:dash')
    fields = ('rtm_code','rtm_desc','rtm_dist','rtm_slno','rtm_remarks','rtm_active','rtm_details')

class FreightforrouteCreate(CreateView):
    model = Freightforroute
    template_name = 'master/freightforroute.html'
    success_url = reverse_lazy('app:dash')
    fields = ('fght_fretypeptr','fght_routeptr','fght_basefreight','fght_kmrate','fght_vehcatptr','fght_slno','fght_remarks','fght_active')



