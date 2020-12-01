from django import forms
<<<<<<< HEAD
from app.models import Tyre, Vehiclemaster, Accessories, Driver, Trip, FuelLog, Tripsheet,Profile
from django.forms import ModelForm, inlineformset_factory, ModelMultipleChoiceField
from django_select2.forms import ModelSelect2Widget
from dal import autocomplete
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
=======
from app.models import Tyre, Vehiclemaster, Accessories, Driver, Trip, FuelLog, Tripsheet
from django.forms import ModelForm, inlineformset_factory, ModelMultipleChoiceField
from django_select2.forms import ModelSelect2Widget
from dal import autocomplete
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b
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
<<<<<<< HEAD
class ProfileCreationForm(UserCreationForm):
    
    class Meta:
        model = Profile
        fields = ('name','usrcatpntr','region','username')

class ProfileChangeForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = ('name', 'password','usrcatpntr','region')
=======
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b

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

<<<<<<< HEAD

class TDriverForm(ModelForm):

	lno = forms.RegexField(regex = "^(([A-Z]{2}[0-9]{2})"
              + "( )|([A-Z]{2}-[0-9]"
              + "{2}))((19|20)[0-9]"
              + "[0-9])[0-9]{7}$") 


	class Meta:
		model= Driver
		is_temp = forms.BooleanField(widget=forms.HiddenInput(), initial=True) 
		fields = ('name','licence', 'lno', 'lexpiry','phone','region','address')

class PDriverForm(ModelForm):

	lno = forms.RegexField(regex = "^(([A-Z]{2}[0-9]{2})"
              + "( )|([A-Z]{2}-[0-9]"
              + "{2}))((19|20)[0-9]"
              + "[0-9])[0-9]{7}$") 


	class Meta:
		model= Driver
		fields = ('name','phone','region','address','salary','photo','licence','lno', 'lexpiry','rationcard','aadhar')
=======
class DriverForm(ModelForm):

	class Meta:
		model= Driver
		exclude = ('bata', 'is_settled','advance','expense')
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b

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
<<<<<<< HEAD
        }


class TripstartForm(ModelForm):

	status = forms.CharField(widget=forms.HiddenInput(), initial=1)
	class Meta:

		model = Trip
		fields = ( 'start',)


	# def __init__(self, *args, **kwargs):
	# 	super(TripstartForm, self).__init__(*args, **kwargs)
	# 	instance = getattr(self, 'instance', None)
	# 	if instance and instance.pk:
	# 		self.fields['veh'].widget.attrs['readonly'] = True
	# 		self.fields['tripno'].widget.attrs['readonly'] = True

class TripendForm(ModelForm):

	status = forms.CharField(widget=forms.HiddenInput(), initial=0)

	# veh = forms.CharField(widget=forms.TextInput)
	class Meta:

		model = Trip
		fields = ( 'end',)

	# def __init__(self, *args, **kwargs):
	# 	super(TripendForm, self).__init__(*args, **kwargs)
	# 	instance = getattr(self, 'instance', None)
	# 	if instance and instance.pk:
	# 		self.fields['veh'].widget.attrs['readonly'] = True
	# 		self.fields['tripno'].widget.attrs['readonly'] = True
=======
        }
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b
