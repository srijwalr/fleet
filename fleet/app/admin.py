from django.contrib import admin
<<<<<<< HEAD
from .models import Vehiclecategory, Vehiclemaster, Freighttypes, Driver, Tyre, Profile, Usercat, Region, Trip, FuelLog
=======
from .models import Vehiclecategory, Vehiclemaster, Freighttypes, Driver, Tyre, Profile, Usercategory
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b
# Register your models here.


class VehiclemasterAdmin(admin.ModelAdmin):
	search_fields = ('vehmas_code', )


admin.site.register(Profile)
<<<<<<< HEAD
admin.site.register(Usercat)
=======
admin.site.register(Usercategory)
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b

admin.site.register(Vehiclecategory)
admin.site.register(Vehiclemaster, VehiclemasterAdmin)
admin.site.register(Freighttypes)
admin.site.register(Driver)
admin.site.register(Tyre)
<<<<<<< HEAD
admin.site.register(FuelLog)
admin.site.register(Trip)
admin.site.register(Region)
=======
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b



