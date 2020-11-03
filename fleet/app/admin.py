from django.contrib import admin
from .models import Vehiclecategory, Vehiclemaster, Freighttypes, Driver, Tyre, Profile, Usercategory
# Register your models here.


class VehiclemasterAdmin(admin.ModelAdmin):
	search_fields = ('vehmas_code', )


admin.site.register(Profile)
admin.site.register(Usercategory)

admin.site.register(Vehiclecategory)
admin.site.register(Vehiclemaster, VehiclemasterAdmin)
admin.site.register(Freighttypes)
admin.site.register(Driver)
admin.site.register(Tyre)



