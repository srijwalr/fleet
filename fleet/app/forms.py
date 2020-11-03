from django import forms
from app.models import Tyre, Vehiclemaster, Accessories, Driver, Trip, FuelLog, Tripsheet
from django.forms import ModelForm, inlineformset_factory, ModelMultipleChoiceField
from django_select2.forms import ModelSelect2Widget
from dal import autocomplete
# from pip import autocomplete


# class VehiclemasterForm(ModelForm):

# 	acc = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Accessories.objects.all())
# 	# acc = forms.ModelMultipleChoiceField(queryset=Accessories.objects.all(),widget=forms.CheckboxSelectMultiple(),required=True)	

# 	class Meta:
# 		model: Vehiclemaster
# 		exclude = ('driver',)

# 	def __init__(self, *args, **kwargs):

# 		super(VehiclemasterForm, self).__init__(*args, **kwargs)
# 		self.fields["acc"].widget = CheckboxSelectMultiple()
# 		self.fields["acc"].queryset = Accessories.objects.all()

class FuelLogForm(ModelForm):

	veh = forms.ModelChoiceField(queryset = Vehiclemaster.objects.all(), widget = autocomplete.ModelSelect2(url='veh-autocomp'))

	class Meta:
		model = FuelLog
		fields = ('veh','no','date','diesel','lub','othr','odo','fuel')

		widgets = {
            'date': forms.DateInput(
                format=('%m/%d/%Y'),
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Select a date',
                    'type': 'date',
                }


            ),
        }
		
class TyreForm(ModelForm):
    class Meta:
        model = Tyre
        exclude = ()

TyreFormSet = inlineformset_factory(Vehiclemaster, Tyre,
                                            form=TyreForm, extra=5)

class DriverForm(ModelForm):

	class Meta:
		model= Driver
		exclude = ('bata', 'is_settled','advance','expense')

class ExpenseForm(ModelForm):

	class Meta:
		model= Driver
		fields = ('name','advance','expense')

class TripsheetForm(ModelForm):

    driver = forms.ModelChoiceField(queryset = Driver.objects.all(), widget = autocomplete.ModelSelect2(url='driver-autocomp'))
    veh = forms.ModelChoiceField(queryset = Vehiclemaster.objects.all(), widget = autocomplete.ModelSelect2(url='veh-autocomp'))

    class Meta:
        model = Tripsheet
        fields = '__all__'

class TripForm(ModelForm):

	driver = forms.ModelChoiceField(queryset = Driver.objects.all(), widget = autocomplete.ModelSelect2(url='driver-autocomp'))
	veh = forms.ModelChoiceField(queryset = Vehiclemaster.objects.all(), widget = autocomplete.ModelSelect2(url='veh-autocomp'))

	class Meta:

		model = Trip
		exclude = ('km','bata','is_approved')
		widgets = {
            'date': forms.DateInput(
                format=('%m/%d/%Y'),
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Select a date',
                    'type': 'date',
                }


            ),
        }