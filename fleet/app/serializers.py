from rest_framework import serializers
from fleet.models import Fleet, Tripsheet, Driver


class FleetSerializer(serializers.ModelSerializer): 

    driver = serializers.RelatedField(read_only=True)

    class Meta:
    	model = Fleet 
    	fields = ['id', 'veh', 'driver'] 

class TripsheetSerializers(serializers.ModelSerializer):	

	class Meta:
		model = Tripsheet
		fields = ['id', 'veh', 'driver']


class DriverSerializers(serializers.ModelSerializer):	

	class Meta:
		model = Driver
		fields = ['id', 'name', 'region']
















































