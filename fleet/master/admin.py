from django.contrib import admin
from .models import Cosingneemaster, Productcategory, Productsubcategory, Productgroup, Productmaster, Vehiclecategory, Vehiclemaster, Freighttypes, Routemaster, Freightforroute, Cosingnormaster

# Register your models here.
admin.site.register(Cosingneemaster)
admin.site.register(Cosingnormaster)
admin.site.register(Productcategory)
admin.site.register(Productsubcategory)
admin.site.register(Productgroup)
admin.site.register(Productmaster)
admin.site.register(Vehiclecategory)
admin.site.register(Vehiclemaster)
admin.site.register(Freighttypes)
admin.site.register(Routemaster)
admin.site.register(Freightforroute)
