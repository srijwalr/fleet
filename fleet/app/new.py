from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings as django_settings
from django.contrib.auth import authenticate, login, logout
from django.urls import reversexc
from django.db.models import Q
from django.views.generic import TemplateView, DetailView, View, ListView, FormView
from django.apps import apps
from django.http import Http404
from . import models
from . import forms
from . import utils
import os
import json
import uuid
import datetime
import pytz

class RegisterView(FormView):
	template_name = "userarea/register.html"
	form_class = forms.RegisterForm

	def get(self, request):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('fleetapp:dashboard'))

		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			uid = uuid.uuid4().hex[:20]
			a = models.Signups(uuid=uid, organization_name=form.cleaned_data['organization_name'],
				full_name=form.cleaned_data['full_name'], email=form.cleaned_data['email'],
				password=form.cleaned_data['password'])
			a.save()
			link = "http://"+str(request.get_host())+"/app/emailconfirm/" + uid + "/"
			template = get_template('emails/email_signup.html')
			html_content = template.render({"confirmlink":link})
			subject = "Please validate your email address."
			utils.send_email(subject,form.cleaned_data['email'],html_content)

			template = get_template('emails/admin_newsignup.html')
			html_content = template.render({
					"organization_name" : form.cleaned_data['organization_name'],
					"fleet_size" : form.cleaned_data['fleet_size'],
					"full_name" : form.cleaned_data['full_name'],
					"email" : form.cleaned_data['email'],
					"phone_number" : form.cleaned_data['phone_number']
				})
			subject = "New Registration At fleet"
			utils.send_email(subject,"aditya@fleethq.com",html_content)

			form = self.form_class(initial=self.initial)
			return render(request, self.template_name, {'form': form , 'form_success':True})
		return render(request, self.template_name, {'form': form})



class EmailConfirmView(View):
	def get(self, request, uid):
		signupobj= get_object_or_404(models.Signups, uuid=uid)
		User.objects.create_user(signupobj.email, signupobj.email, signupobj.password)
		user = authenticate(username=signupobj.email, password=signupobj.password)
		ac = models.Account.objects.create(owner = user, organization_name=signupobj.organization_name)
		models.Contact.objects.create(user=user, account=ac, full_name=signupobj.full_name, is_owner=True, is_user=True)
		login(request,user)
		signupobj.delete()
		return HttpResponseRedirect(reverse('fleetapp:dashboard'))



class ForgotPasswordView(FormView):
	template_name = "userarea/forgotpassword.html"
	form_class = forms.ForgotPasswordForm

	def get(self, request):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('fleetapp:dashboard'))
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			uid = uuid.uuid4().hex[:20]
			u = User.objects.get(email = form.cleaned_data["email"])
			u.set_password(uid)
			u.save()
			template = get_template('emails/email_forgotpassword.html')
			html_content = template.render({"newpassword":uid})
			subject = "Your new password at fleet"
			utils.send_email(subject,form.cleaned_data["email"],html_content)
			form = self.form_class(initial=self.initial)
			return render(request, self.template_name, {'form': form , 'form_success':True})
		return render(request, self.template_name, {'form': form})



class LoginView(FormView):
	template_name = "userarea/login.html"
	form_class = forms.LoginForm

	def get(self, request):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('fleetapp:dashboard'))
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			#k = get_object_or_404(User, email=form.cleaned_data["email"])
			#if not user.contact.is_user:
			#	return HttpResponseRedirect(reverse('fleetapp:login'))

			user = authenticate(username=form.cleaned_data["email"], password=form.cleaned_data["password"])
			if user==None:
				return render(request, self.template_name, {'form': form , 'other_error':"Incorrect password"})
			else:
				login(request, user)
				return HttpResponseRedirect(reverse('fleetapp:dashboard'))

		return render(request, self.template_name, {'form': form})



@method_decorator(login_required, name='dispatch')
class LogoutView(View):
	def get(self, request):
		logout(request)	
		return HttpResponseRedirect(reverse('fleetapp:login'))


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class FileUploadView(View):
	def post(self, request, *args, **kwargs):
		models.Files.objects.create(account = request.user.contact.account,
			url=request.POST.get('url',''),
			file_type=request.POST.get('file_type',''),
			linked_object_type=request.POST.get('linked_object_type',''),
			linked_object_id=request.POST.get('linked_object_id',''),
			name =request.POST.get('name',''),
			uuid =request.POST.get('uuid',''),
			uploaded_by = request.user.contact
		)
		return HttpResponse("true")


@method_decorator(login_required, name='dispatch')
class CommentAddView(View):
	def get(self, request, object_id, object_type):
		if object_type not in ['Vehicle','Issues','ServiceReminders','VehicleRenewalReminder','FuelEntry','ServiceEntry','Contact']:
			raise Http404
		mymodel = apps.get_model('fleetApp', object_type)
		myobject = get_object_or_404(mymodel, pk=object_id)
		form = forms.CommentForm()
		return render(request, "userarea/add_comment.html", {'form':form, 'page_title':'Add Comment To '+object_type+' #'+str(object_id) })
	def post(self, request, object_id, object_type, *args, **kwargs):
		if object_type not in ['Vehicle','Issues','ServiceReminders','VehicleRenewalReminder','FuelEntry','ServiceEntry','Contact']:
			raise Http404
		mymodel = apps.get_model('fleetApp', object_type)
		myobject = get_object_or_404(mymodel, pk=object_id)		
		form = forms.CommentForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.author = self.request.user.contact
			instance.linked_object_type = object_type
			instance.linked_object_id = object_id
			instance.save()
			return HttpResponseRedirect(request.GET.get('next'))
		return render(request, "userarea/add_comment.html", {'form':form, 'page_title':'Add Comment To '+object_type+' #'+str(object_id) })


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
	template_name = "userarea/dashboard.html"



@method_decorator(login_required, name='dispatch')
class VehicleListView(ListView):
	model = models.Vehicle
	template_name = "userarea/vehicles/vehicle_list.html"
	def get_queryset(self):
		queryset = models.Vehicle.objects.filter(account=self.request.user.contact.account)
		return queryset



@method_decorator(login_required, name='dispatch')
class VehicleDetailView(DetailView):
	model = models.Vehicle
	template_name = "userarea/vehicles/vehicle_detail.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		odometer_latest = models.OdometerEntry.objects.filter(account=self.request.user.contact.account,
				vehicle__id = self.kwargs['pk']
			).order_by('-id').first()
		context['odometer_latest'] = odometer_latest
		context['vehicledetails']=True
		return context


@method_decorator(login_required, name='dispatch')
class VehicleEditView(View):
	def get(self, request, pk):
		object = get_object_or_404(models.Vehicle, pk=pk)
		form = forms.VehicleForm(instance=object)
		form.fields['vehicle_type'].queryset = models.MasterVehicleTypes.objects.filter(account=self.request.user.contact.account)
		form.fields['status'].queryset = models.MasterVehicleStatus.objects.filter(account=self.request.user.contact.account)
		form.fields['make'].queryset = models.MasterMakes.objects.filter(account=self.request.user.contact.account)
		form.fields['profilepicture'].queryset = models.Files.objects.filter(account=self.request.user.contact.account, 
			file_type='IMAGE', linked_object_type='Vehicle', linked_object_id=pk)
		form.fields['model'].queryset = models.MasterModels.objects.filter(account=self.request.user.contact.account)
		form.fields['assigned_to'].queryset = models.Contact.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/vehicles/vehicle_edit.html", {'object': object, 'form':form, 'page_title':'Edit Vehicle' , 'vehicledetails':True})
	def post(self, request, pk, *args, **kwargs):
		object = get_object_or_404(models.Vehicle, pk=pk)	
		form = forms.VehicleForm(request.POST, instance=object)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('fleetapp:vehicledetail',args=[pk]))
		return render(request, "userarea/vehicles/vehicle_edit.html", {'object': object, 'form':form, 'page_title':'Edit Vehicle' , 'vehicledetails':True})



@method_decorator(login_required, name='dispatch')
class VehicleAddView(View):
	def get(self, request):
		form = forms.VehicleForm()
		form.fields.pop('profilepicture')
		form.fields['vehicle_type'].queryset = models.MasterVehicleTypes.objects.filter(account=self.request.user.contact.account)
		form.fields['status'].queryset = models.MasterVehicleStatus.objects.filter(account=self.request.user.contact.account)
		form.fields['make'].queryset = models.MasterMakes.objects.filter(account=self.request.user.contact.account)
		form.fields['model'].queryset = models.MasterModels.objects.filter(account=self.request.user.contact.account)
		form.fields['assigned_to'].queryset = models.Contact.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/vehicles/vehicle_new.html", {'object': object, 'form':form, 'page_title':'Add Vehicle'})
	def post(self, request, *args, **kwargs):
		form = forms.VehicleForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			return HttpResponseRedirect(reverse('fleetapp:vehicledetail',args=[instance.pk]))
		return render(request, "userarea/vehicles/vehicle_new.html", {'object': object, 'form':form, 'page_title':'Edit Vehicle'})



@method_decorator(login_required, name='dispatch')
class VehicleFilesView(DetailView):
	model = models.Vehicle
	template_name = "userarea/vehicles/vehicle_files.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['files'] = models.Files.objects.filter(account=self.request.user.contact.account,
				linked_object_type = 'Vehicle',
				linked_object_id=self.kwargs['pk']
			).order_by('-upload_timestamp')
		context['vehiclefiles']=True		
		return context



@method_decorator(login_required, name='dispatch')
class VehicleCommentsView(DetailView):
	model = models.Vehicle
	template_name = "userarea/vehicles/vehicle_comments.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['comments'] = models.Comments.objects.filter(account=self.request.user.contact.account,
				linked_object_type = 'Vehicle',
				linked_object_id=self.kwargs['pk']
			).order_by('-timestamp')
		context['vehiclecomments']=True		
		return context


@method_decorator(login_required, name='dispatch')
class VehicleAllRemindersView(DetailView):
	model = models.Vehicle
	template_name = "userarea/vehicles/vehicle_allreminders.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		querydata = models.VehicleRenewalReminder.objects.filter(account=self.request.user.contact.account,
				vehicle__id = self.kwargs['pk']
			)
		objectlist = []
		for q in querydata:
			k = q.due_date - timezone.now().date()
			if k.days > q.days_treshold:
				status="scheduled"
			if k.days <= q.days_treshold:
				status="duesoon"
			if k.days < 0:
				status="overdue"
			q.status = status
			objectlist.append(q)
		context['vehiclerenewalreminders'] = objectlist
		querydata = models.ServiceReminders.objects.filter(account=self.request.user.contact.account,
				vehicle__id = self.kwargs['pk']
			)
		objectlist = []
		for q in querydata:
			odometer_latest = models.OdometerEntry.objects.filter(account=self.request.user.contact.account,
				vehicle = q.vehicle).order_by('-id').first()
			k = q.odometer_reading - q.odometer_treshold
			if odometer_latest.reading < k:
				q.status = "scheduled"
			if odometer_latest.reading >= k:
				q.status = "duesoon"
			if odometer_latest.reading > q.odometer_reading:
				q.status = "overdue"
			objectlist.append(q)
		context['servicereminders'] = objectlist

		context['reminderstab']=True		
		return context



@method_decorator(login_required, name='dispatch')
class VehicleAllIssues(DetailView):
	model = models.Vehicle
	template_name = "userarea/vehicles/vehicle_allissues.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['vehicleissues'] = models.Issues.objects.filter(account=self.request.user.contact.account,
				vehicle__id = self.kwargs['pk']
			)
		context['vehicleissuestab']=True		
		return context


@method_decorator(login_required, name='dispatch')
class VehicleAllFuelEnties(DetailView):
	model = models.Vehicle
	template_name = "userarea/vehicles/vehicle_allfuelentries.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['vehiclefuelentries'] = models.FuelEntry.objects.filter(account=self.request.user.contact.account,
				vehicle__id = self.kwargs['pk']
			)
		context['vehiclefuelentriestab']=True		
		return context


@method_decorator(login_required, name='dispatch')
class VehicleAllServiceEntries(DetailView):
	model = models.Vehicle
	template_name = "userarea/vehicles/vehicle_allserviceentries.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['vehicleserviceentries'] = models.ServiceEntry.objects.filter(account=self.request.user.contact.account,
				vehicle__id = self.kwargs['pk']
			)
		context['vehicleserviceentriestab']=True		
		return context

@method_decorator(login_required, name='dispatch')
class VehicleOdometerHistory(DetailView):
	model = models.Vehicle
	template_name = "userarea/vehicles/vehicle_odometerhistory.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['odometerhistory'] = models.OdometerEntry.objects.filter(account=self.request.user.contact.account,
				vehicle__id = self.kwargs['pk']
			).order_by('-id')
		context['odometerhistorytab']=True		
		return context



@method_decorator(login_required, name='dispatch')
class OdometerEntryAdd(View):
	def get(self, request, pk):
		object = get_object_or_404(models.Vehicle, pk=pk)
		form = forms.OdometerEntryForm(initial={'vehicle':object})
		form.fields['vehicle'].queryset = models.Vehicle.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/vehicles/odometer_new.html", {'form':form, 'page_title':'Add New Odometer Entry'})
	def post(self, request, pk, *args, **kwargs):
		form = forms.OdometerEntryForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.reported_by = self.request.user.contact
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:odometerhistory', args=[pk]))
		return render(request, "userarea/vehicles/odometer_new.html", {'form':form, 'page_title':'Add New Odometer Entry'})


@method_decorator(login_required, name='dispatch')
class VehicleRenewalReminderDetail(View):
	def get(self, request, pk):
		template_name = "userarea/vehicles/detail_vehiclereminder.html"
		context={}
		obj = get_object_or_404(models.VehicleRenewalReminder, pk=self.kwargs['pk'])
		k = obj.due_date - timezone.now().date()
		if k.days > obj.days_treshold:
			status="scheduled"
		if k.days <= obj.days_treshold:
			status="duesoon"
		if k.days < 0:
			status="overdue"
		obj.status = status
		context['vehiclerenewalreminderdetail'] = obj
		context['object'] = get_object_or_404(models.Vehicle, pk=context['vehiclerenewalreminderdetail'].vehicle.id)
		context['comments'] = models.Comments.objects.filter(account=self.request.user.contact.account,
				linked_object_type = 'VehicleRenewalReminder',
				linked_object_id=self.kwargs['pk']
			).order_by('-timestamp')
		context['files'] = models.Files.objects.filter(account=self.request.user.contact.account,
				linked_object_type = 'VehicleRenewalReminder',
				linked_object_id=self.kwargs['pk']
			).order_by('-upload_timestamp')
		context['reminderstab']=True		
		return render(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class ServiceReminderDetail(View):
	def get(self, request, pk):
		template_name = "userarea/vehicles/detail_servicereminder.html"
		context={}
		obj = get_object_or_404(models.ServiceReminders, pk=self.kwargs['pk'])
		vehicleobj = obj.vehicle

		odometer_latest = models.OdometerEntry.objects.filter(account=self.request.user.contact.account,
			vehicle = vehicleobj).order_by('-id').first()
		k = obj.odometer_reading - obj.odometer_treshold
		if odometer_latest.reading < k:
			obj.status = "scheduled"
		if odometer_latest.reading >= k:
			obj.status = "duesoon"
		if odometer_latest.reading > obj.odometer_reading:
			obj.status = "overdue"

		context['servicereminderdetail'] = obj
		context['object'] = vehicleobj
		context['comments'] = models.Comments.objects.filter(account=self.request.user.contact.account,
				linked_object_type = 'ServiceReminders',
				linked_object_id=self.kwargs['pk']
			).order_by('-timestamp')
		context['files'] = models.Files.objects.filter(account=self.request.user.contact.account,
				linked_object_type = 'ServiceReminders',
				linked_object_id=self.kwargs['pk']
			).order_by('-upload_timestamp')

		context['reminderstab']=True		
		return render(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class IssueDetail(View):
	def get(self, request, pk):
		template_name = "userarea/vehicles/detail_issue.html"
		context={}
		context['issuedetail'] = get_object_or_404(models.Issues, pk=self.kwargs['pk'])
		context['object'] = get_object_or_404(models.Vehicle, pk=context['issuedetail'].vehicle.id)
		context['comments'] = models.Comments.objects.filter(account=self.request.user.contact.account,
				linked_object_type = 'Issues',
				linked_object_id=self.kwargs['pk']
			).order_by('-timestamp')
		context['files'] = models.Files.objects.filter(account=self.request.user.contact.account,
				linked_object_type = 'Issues',
				linked_object_id=self.kwargs['pk']
			).order_by('-upload_timestamp')
		context['vehicleissuestab']=True		
		return render(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class ServiceEntryDetail(View):
	def get(self, request, pk):
		template_name = "userarea/vehicles/detail_serviceentry.html"
		context={}
		context['serviceentrydetail'] = get_object_or_404(models.ServiceEntry, pk=self.kwargs['pk'])
		context['object'] = get_object_or_404(models.Vehicle, pk=context['serviceentrydetail'].vehicle.id)
		context['comments'] = models.Comments.objects.filter(account=self.request.user.contact.account,
				linked_object_type = 'ServiceEntry',
				linked_object_id=self.kwargs['pk']
			).order_by('-timestamp')
		context['files'] = models.Files.objects.filter(account=self.request.user.contact.account,
				linked_object_type = 'ServiceEntry',
				linked_object_id=self.kwargs['pk']
			).order_by('-upload_timestamp')
		context['vehicleserviceentriestab']=True		
		return render(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class FuelEntryDetail(View):
	def get(self, request, pk):
		template_name = "userarea/vehicles/detail_fuelentry.html"
		context={}
		context['fuelentrydetail'] = get_object_or_404(models.FuelEntry, pk=self.kwargs['pk'])
		context['object'] = get_object_or_404(models.Vehicle, pk=context['fuelentrydetail'].vehicle.id)
		context['comments'] = models.Comments.objects.filter(account=self.request.user.contact.account,
				linked_object_type = 'FuelEntry',
				linked_object_id=self.kwargs['pk']
			).order_by('-timestamp')
		context['files'] = models.Files.objects.filter(account=self.request.user.contact.account,
				linked_object_type = 'FuelEntry',
				linked_object_id=self.kwargs['pk']
			).order_by('-upload_timestamp')

		context['vehiclefuelentriestab']=True		
		return render(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class VehicleRenewalReminderListView(ListView):
	model = models.VehicleRenewalReminder	
	template_name = "userarea/reminders/vehiclerenewalreminders.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		querydata = models.VehicleRenewalReminder.objects.filter(account=self.request.user.contact.account)
		objectlist = []
		for q in querydata:
			k = q.due_date - timezone.now().date()
			if k.days > q.days_treshold:
				status="scheduled"
			if k.days <= q.days_treshold:
				status="duesoon"
			if k.days < 0:
				status="overdue"
			q.status = status
			objectlist.append(q)
		context['object_list'] = objectlist
		return context




@method_decorator(login_required, name='dispatch')
class VehicleRenewalReminderAddView(View):
	def get(self, request, pk):
		if pk > 0:
			object = get_object_or_404(models.Vehicle, pk=pk)
			form = forms.VehicleRenewalReminderForm(initial={'vehicle':object})
		else:
			form = forms.VehicleRenewalReminderForm()
		form.fields['vehicle'].queryset = models.Vehicle.objects.filter(account=self.request.user.contact.account)
		form.fields['vehicle_reminder_type'].queryset = models.MasterVehicleRenewalReminderType.objects.filter(account=self.request.user.contact.account)
		form.fields['notify_contacts'].queryset = models.Contact.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/reminders/vehiclerenewalreminder_new.html", {'form':form, 'page_title':'Add Vehicle Renewal Reminder'})
	def post(self, request, *args, **kwargs):
		form = forms.VehicleRenewalReminderForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:vehiclerenewalreminderdetail', args=[instance.id]))
		return render(request, "userarea/reminders/vehiclerenewalreminder_new.html", {'form':form, 'page_title':'Add Vehicle Renewal Reminder'})



@method_decorator(login_required, name='dispatch')
class VehicleRenewalReminderEditView(View):
	def get(self, request, pk):
		object = get_object_or_404(models.VehicleRenewalReminder, pk=pk)
		form = forms.VehicleRenewalReminderForm(instance=object)
		form.fields['vehicle'].queryset = models.Vehicle.objects.filter(account=self.request.user.contact.account)
		form.fields['vehicle_reminder_type'].queryset = models.MasterVehicleRenewalReminderType.objects.filter(account=self.request.user.contact.account)
		form.fields['notify_contacts'].queryset = models.Contact.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/reminders/vehiclerenewalreminder_new.html", {'form':form, 'page_title':'Edit Vehicle Renewal Reminder'})
	def post(self, request, pk, *args, **kwargs):
		object = get_object_or_404(models.VehicleRenewalReminder, pk=pk)
		form = forms.VehicleRenewalReminderForm(request.POST, instance=object)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:vehiclerenewalreminderdetail', args=[instance.id]))
		return render(request, "userarea/reminders/vehiclerenewalreminder_new.html", {'form':form, 'page_title':'Edit Vehicle Renewal Reminder'})


@method_decorator(login_required, name='dispatch')
class ServiceReminderListView(ListView):
	model = models.ServiceReminders	
	template_name = "userarea/reminders/servicereminders.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		querydata = models.ServiceReminders.objects.filter(account=self.request.user.contact.account)
		objectlist = []
		for q in querydata:
			odometer_latest = models.OdometerEntry.objects.filter(account=self.request.user.contact.account,
				vehicle = q.vehicle).order_by('-id').first()
			k = q.odometer_reading - q.odometer_treshold
			if odometer_latest.reading < k:
				q.status = "scheduled"
			if odometer_latest.reading >= k:
				q.status = "duesoon"
			if odometer_latest.reading > q.odometer_reading:
				q.status = "overdue"
			objectlist.append(q)
		context['object_list'] = objectlist
		return context


@method_decorator(login_required, name='dispatch')
class ServiceReminderAddView(View):
	def get(self, request, pk):
		if pk > 0:
			object = get_object_or_404(models.Vehicle, pk=pk)
			form = forms.ServiceReminderForm(initial={'vehicle':object})
		else:
			form = forms.ServiceReminderForm()
		form.fields['vehicle'].queryset = models.Vehicle.objects.filter(account=self.request.user.contact.account)
		form.fields['service_reminder_type'].queryset = models.MasterServiceReminderTypes.objects.filter(account=self.request.user.contact.account)
		form.fields['notify_contacts'].queryset = models.Contact.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/reminders/servicereminder_new.html", {'form':form, 'page_title':'Add Service Reminder'})
	def post(self, request, *args, **kwargs):
		form = forms.ServiceReminderForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:servicereminderdetail', args=[instance.id]))
		return render(request, "userarea/reminders/servicereminder_new.html", {'form':form, 'page_title':'Add Service Reminder'})



@method_decorator(login_required, name='dispatch')
class ServiceReminderEditView(View):
	def get(self, request, pk):
		object = get_object_or_404(models.ServiceReminders, pk=pk)
		form = forms.ServiceReminderForm(instance=object)
		form.fields['vehicle'].queryset = models.Vehicle.objects.filter(account=self.request.user.contact.account)
		form.fields['service_reminder_type'].queryset = models.MasterServiceReminderTypes.objects.filter(account=self.request.user.contact.account)
		form.fields['notify_contacts'].queryset = models.Contact.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/reminders/servicereminder_new.html", {'form':form, 'page_title':'Edit Service Reminder'})
	def post(self, request, pk, *args, **kwargs):
		object = get_object_or_404(models.ServiceReminders, pk=pk)
		form = forms.ServiceReminderForm(request.POST, instance=object)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:servicereminderdetail', args=[instance.id]))
		return render(request, "userarea/reminders/servicereminder_new.html", {'form':form, 'page_title':'Edit Service Reminder'})


@method_decorator(login_required, name='dispatch')
class IssuesListView(ListView):
	model = models.Issues	
	template_name = "userarea/issues/issues.html"
	def get_queryset(self):
		queryset = models.Issues.objects.filter(account=self.request.user.contact.account)
		return queryset


@method_decorator(login_required, name='dispatch')
class IssueAddView(View):
	def get(self, request, pk):
		if pk > 0:
			object = get_object_or_404(models.Vehicle, pk=pk)
			form = forms.IssueForm(initial={'vehicle':object})
		else:
			form = forms.IssueForm()
		form.fields['vehicle'].queryset = models.Vehicle.objects.filter(account=self.request.user.contact.account)
		form.fields['reported_by'].queryset = models.Contact.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/issues/issue_new.html", {'form':form, 'page_title':'Add Issue'})
	def post(self, request, *args, **kwargs):
		form = forms.IssueForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:issuedetail', args=[instance.id]))
		return render(request, "userarea/issues/issue_new.html", {'form':form, 'page_title':'Add Issue'})



@method_decorator(login_required, name='dispatch')
class IssueEditView(View):
	def get(self, request, pk):
		object = get_object_or_404(models.Issues, pk=pk)
		form = forms.IssueForm(instance=object)
		form.fields['vehicle'].queryset = models.Vehicle.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/issues/issue_new.html", {'form':form, 'page_title':'Edit Issue'})
	def post(self, request, pk, *args, **kwargs):
		object = get_object_or_404(models.Issues, pk=pk)
		form = forms.IssueForm(request.POST, instance=object)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:issuedetail', args=[instance.id]))
		return render(request, "userarea/issues/issue_new.html", {'form':form, 'page_title':'Edit Issue'})



@method_decorator(login_required, name='dispatch')
class VendorsListView(ListView):
	model = models.Vendors	
	template_name = "userarea/vendors/vendors.html"
	def get_queryset(self):
		queryset = models.Vendors.objects.filter(account=self.request.user.contact.account)
		return queryset


@method_decorator(login_required, name='dispatch')
class VendorsAddView(View):
	def get(self, request):
		form = forms.VendorsForm()
		form.fields['vendor_type'].queryset = models.MasterVendorTypes.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/vendors/vendors_new.html", {'form':form, 'page_title':'Add Vendor'})
	def post(self, request, *args, **kwargs):
		form = forms.VendorsForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:vendors'))
		return render(request, "userarea/issues/issue_new.html", {'form':form, 'page_title':'Add Vendor'})



@method_decorator(login_required, name='dispatch')
class VendorsEditView(View):
	def get(self, request, pk):
		object = get_object_or_404(models.Vendors, pk=pk)
		form = forms.VendorsForm(instance=object)
		form.fields['vendor_type'].queryset = models.MasterVendorTypes.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/vendors/vendors_new.html", {'form':form, 'page_title':'Edit Vendor'})
	def post(self, request, pk, *args, **kwargs):
		object = get_object_or_404(models.Vendors, pk=pk)
		form = forms.VendorsForm(request.POST, instance=object)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:vendors'))
		return render(request, "userarea/vendors/vendors_new.html", {'form':form, 'page_title':'Edit Vendor'})


@method_decorator(login_required, name='dispatch')
class FuelEntryListView(ListView):
	model = models.FuelEntry	
	template_name = "userarea/fuelentries/fuelentries.html"
	def get_queryset(self):
		queryset = models.FuelEntry.objects.filter(account=self.request.user.contact.account)
		return queryset


@method_decorator(login_required, name='dispatch')
class FuelEntryAddView(View):
	def get(self, request,pk):
		if pk > 0:
			object = get_object_or_404(models.Vehicle, pk=pk)
			form = forms.FuelEntryForm(initial={'vehicle':object})
		else:
			form = forms.FuelEntryForm()
		form.fields['vendor'].queryset = models.Vendors.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/fuelentries/fuelentries_new.html", {'form':form, 'page_title':'Add Fuel Entry'})
	def post(self, request, *args, **kwargs):
		form = forms.FuelEntryForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:fuelentrydetail', args=[instance.id]))
		return render(request, "userarea/fuelentries/fuelentries_new.html", {'form':form, 'page_title':'Add Fuel Entry'})



@method_decorator(login_required, name='dispatch')
class FuelEntryEditView(View):
	def get(self, request, pk):
		object = get_object_or_404(models.FuelEntry, pk=pk)
		form = forms.FuelEntryForm(instance=object)
		form.fields['vendor'].queryset = models.Vendors.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/fuelentries/fuelentries_new.html", {'form':form, 'page_title':'Edit Fuel Entry'})
	def post(self, request, pk, *args, **kwargs):
		object = get_object_or_404(models.FuelEntry, pk=pk)
		form = forms.FuelEntryForm(request.POST, instance=object)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:fuelentrydetail', args=[instance.id]))
		return render(request, "userarea/fuelentries/fuelentries_new.html", {'form':form, 'page_title':'Edit Fuel Entry'})



@method_decorator(login_required, name='dispatch')
class ServiceEntryListView(ListView):
	model = models.ServiceEntry	
	template_name = "userarea/serviceentries/serviceentries.html"
	def get_queryset(self):
		queryset = models.ServiceEntry.objects.filter(account=self.request.user.contact.account)
		return queryset


@method_decorator(login_required, name='dispatch')
class ServiceEntryAddView(View):
	def get(self, request,pk):
		if pk > 0:
			object = get_object_or_404(models.Vehicle, pk=pk)
			form = forms.ServiceEntryForm(initial={'vehicle':object})
		else:
			form = forms.ServiceEntryForm()
		form.fields['vendor'].queryset = models.Vendors.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/serviceentries/serviceentries_new.html", {'form':form, 'page_title':'Add Service Entry'})
	def post(self, request, *args, **kwargs):
		form = forms.ServiceEntryForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:serviceentrydetail', args=[instance.id]))
		return render(request, "userarea/serviceentries/serviceentries_new.html", {'form':form, 'page_title':'Add Service Entry'})



@method_decorator(login_required, name='dispatch')
class ServiceEntryEditView(View):
	def get(self, request, pk):
		object = get_object_or_404(models.ServiceEntry, pk=pk)
		form = forms.ServiceEntryForm(instance=object)
		form.fields['vendor'].queryset = models.Vendors.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/serviceentries/serviceentries_new.html", {'form':form, 'page_title':'Edit Service Entry'})
	def post(self, request, pk, *args, **kwargs):
		object = get_object_or_404(models.ServiceEntry, pk=pk)
		form = forms.ServiceEntryForm(request.POST, instance=object)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:serviceentrydetail', args=[instance.id]))
		return render(request, "userarea/serviceentries/serviceentries_new.html", {'form':form, 'page_title':'Edit Service Entry'})


@method_decorator(login_required, name='dispatch')
class ContactListView(ListView):
	model = models.Contact	
	template_name = "userarea/contacts/contacts.html"
	def get_queryset(self):
		queryset = models.Contact.objects.filter(account=self.request.user.contact.account)
		return queryset

@method_decorator(login_required, name='dispatch')
class ContactAddView(View):
	def get(self, request):
		form = forms.ContactForm()
		form.fields.pop('profilepicture')
		return render(request, "userarea/contacts/contacts_new.html", {'form':form, 'page_title':'Add Contact'})
	def post(self, request, *args, **kwargs):
		form = forms.ContactForm(request.POST)
		if form.is_valid():
			uid = uuid.uuid4().hex[:20]
			user = User.objects.create_user(form.cleaned_data['email'], form.cleaned_data['email'], uid)
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.user = user
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:contactdetail',args=[instance.id]))
		return render(request, "userarea/contacts/contacts_new.html", {'form':form, 'page_title':'Add Contact'})



@method_decorator(login_required, name='dispatch')
class ContactEditView(View):
	def get(self, request, pk):
		object = get_object_or_404(models.Contact, pk=pk)
		form = forms.ContactForm(instance=object, initial={'email':object.user.email})
		form.fields['profilepicture'].queryset = models.Files.objects.filter(account=self.request.user.contact.account, 
			file_type='IMAGE', linked_object_type='Contact', linked_object_id=pk)
		return render(request, "userarea/contacts/contacts_new.html", {'form':form, 'page_title':'Edit Contact'})
	def post(self, request, pk, *args, **kwargs):
		object = get_object_or_404(models.Contact, pk=pk)
		form = forms.ContactForm(request.POST, instance=object)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			instance.user.email = form.cleaned_data['email']
			instance.user.username = form.cleaned_data['email']
			instance.user.save()
			return HttpResponseRedirect(reverse('fleetapp:contactdetail',args=[instance.id]))
		return render(request, "userarea/contacts/contacts_new.html", {'form':form, 'page_title':'Edit Contact'})


@method_decorator(login_required, name='dispatch')
class ContactDetailView(DetailView):
	model = models.Contact
	template_name = "userarea/contacts/contact_detail.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['comments'] = models.Comments.objects.filter(account=self.request.user.contact.account,
				linked_object_type = 'Contact',
				linked_object_id=self.kwargs['pk']
			).order_by('-timestamp')
		context['files'] = models.Files.objects.filter(account=self.request.user.contact.account,
				linked_object_type = 'Contact',
				linked_object_id=self.kwargs['pk']
			).order_by('-upload_timestamp')

		context['contactdetail']=True
		return context


@method_decorator(login_required, name='dispatch')
class ContactPasswordEditView(View):
	def get(self, request, pk):
		form = forms.ContactPasswordForm()
		return render(request, "userarea/contacts/contact_password.html", {'form':form, 'page_title':'Edit Password For Contact #'+str(pk)})
	def post(self, request, pk, *args, **kwargs):
		object = get_object_or_404(models.Contact, pk=pk)
		form = forms.ContactPasswordForm(request.POST)
		if form.is_valid():
			object.user.set_password(form.cleaned_data['password'])
			object.user.save()
			return HttpResponseRedirect(reverse('fleetapp:contactdetail',args=[pk]))
		return render(request, "userarea/contacts/contact_password.html", {'form':form, 'page_title':'Edit Password For Contact #'+str(pk)})



@method_decorator(login_required, name='dispatch')
class SettingsEditView(View):
	def get(self, request):
		object = get_object_or_404(models.Account, pk=request.user.contact.account.id)
		form = forms.AccountForm(instance=object)
		return render(request, "userarea/settings.html", {'form':form, 'page_title':'Edit Settings'})
	def post(self, request, *args, **kwargs):
		object = get_object_or_404(models.Account, pk=request.user.contact.account.id)
		form = forms.AccountForm(request.POST, instance=object)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:settingsedit'))
		return render(request, "userarea/settings.html", {'form':form, 'page_title':'Edit Settings'})


@method_decorator(login_required, name='dispatch')
class ReportListView(TemplateView):
	template_name = "userarea/reports.html"

@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
	template_name = "userarea/profile.html"


@method_decorator(login_required, name='dispatch')
class MasterVehicleTypesEdit(View):
	def get(self, request):
		form = forms.MasterVehicleTypesForm()
		object_list = models.MasterVehicleTypes.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/master/vehicletypes.html", {'form':form, 'page_title':'Add New Vehicle Type', 'object_list':object_list})
	def post(self, request, *args, **kwargs):
		form = forms.MasterVehicleTypesForm(request.POST)
		object_list = models.MasterVehicleTypes.objects.filter(account=self.request.user.contact.account)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:mastervehicletypesedit'))
		return render(request, "userarea/master/vehicletypes.html", {'form':form, 'page_title':'Add New Vehicle Type', 'object_list':object_list})

@method_decorator(login_required, name='dispatch')
class MasterVehicleStatusEdit(View):
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:fuelentrydetail', args=[instance.id]))
		return render(request, "userarea/fuelentries/fuelentries_new.html", {'form':form, 'page_title':'Edit Fuel Entry'})

	def get(self, request):
		form = forms.MasterVehicleStatusForm()
		object_list = models.MasterVehicleStatus.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/master/vehiclestatus.html", {'form':form, 'page_title':'Add New Vehicle Status', 'object_list':object_list})
	def post(self, request, *args, **kwargs):
		form = forms.MasterVehicleStatusForm(request.POST)
		object_list = models.MasterVehicleStatus.objects.filter(account=self.request.user.contact.account)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:mastervehiclestatusedit'))
		return render(request, "userarea/master/vehicletypes.html", {'form':form, 'page_title':'Add New Vehicle Status', 'object_list':object_list})


@method_decorator(login_required, name='dispatch')
class MasterMakesEdit(View):
	def get(self, request):
		form = forms.MasterMakesForm()
		object_list = models.MasterMakes.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/master/vehiclemakes.html", {'form':form, 'page_title':'Add New Vehicle Make', 'object_list':object_list})
	def post(self, request, *args, **kwargs):
		form = forms.MasterMakesForm(request.POST)
		object_list = models.MasterMakes.objects.filter(account=self.request.user.contact.account)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:mastermakesedit'))
		return render(request, "userarea/master/vehiclemakes.html", {'form':form, 'page_title':'Add New Vehicle Make', 'object_list':object_list})


@method_decorator(login_required, name='dispatch')
class MasterModelsEdit(View):
	def get(self, request):
		form = forms.MasterModelsForm()
		form.fields['vehicle_make'].queryset = models.MasterMakes.objects.filter(account=self.request.user.contact.account)
		object_list = models.MasterModels.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/master/vehiclemodels.html", {'form':form, 'page_title':'Add New Vehicle Model', 'object_list':object_list})
	def post(self, request, *args, **kwargs):
		form = forms.MasterModelsForm(request.POST)
		object_list = models.MasterModels.objects.filter(account=self.request.user.contact.account)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:mastermodelsedit'))
		return render(request, "userarea/master/vehiclemodels.html", {'form':form, 'page_title':'Add New Vehicle Model', 'object_list':object_list})


@method_decorator(login_required, name='dispatch')
class MasterVehicleRenewalReminderTypeEdit(View):
	def get(self, request):
		form = forms.MasterVehicleRenewalReminderTypeForm()
		object_list = models.MasterVehicleRenewalReminderType.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/master/vehiclerenewalremindertypes.html", {'form':form, 'page_title':'Add New Vehicle Renewal Reminder Type', 'object_list':object_list})
	def post(self, request, *args, **kwargs):
		form = forms.MasterVehicleRenewalReminderTypeForm(request.POST)
		object_list = models.MasterVehicleRenewalReminderType.objects.filter(account=self.request.user.contact.account)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:mastervehiclerenewalremindertypeedit'))
		return render(request, "userarea/master/vehiclerenewalremindertypes.html", {'form':form, 'page_title':'Add New Vehicle Renewal Reminder Type', 'object_list':object_list})


@method_decorator(login_required, name='dispatch')
class MasterServiceReminderTypesEdit(View):
	def get(self, request):
		form = forms.MasterServiceReminderTypesForm()
		object_list = models.MasterServiceReminderTypes.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/master/serviceremindertypes.html", {'form':form, 'page_title':'Add New Service Reminder Type', 'object_list':object_list})
	def post(self, request, *args, **kwargs):
		form = forms.MasterServiceReminderTypesForm(request.POST)
		object_list = models.MasterServiceReminderTypes.objects.filter(account=self.request.user.contact.account)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:masterserviceremindertypesedit'))
		return render(request, "userarea/master/serviceremindertypes.html", {'form':form, 'page_title':'Add New Service Reminder Type', 'object_list':object_list})


@method_decorator(login_required, name='dispatch')
class MasterVendorTypesEdit(View):
	def get(self, request):
		form = forms.MasterVendorTypesForm()
		object_list = models.MasterVendorTypes.objects.filter(account=self.request.user.contact.account)
		return render(request, "userarea/master/vendortypes.html", {'form':form, 'page_title':'Add New Vendor Type', 'object_list':object_list})
	def post(self, request, *args, **kwargs):
		form = forms.MasterVendorTypesForm(request.POST)
		object_list = models.MasterVendorTypes.objects.filter(account=self.request.user.contact.account)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.account = self.request.user.contact.account
			instance.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('fleetapp:mastervendortypesedit'))
		return render(request, "userarea/master/vendortypes.html", {'form':form, 'page_title':'Add New Vendor Type', 'object_list':object_list})

<div class="jumbotron jumbotron-fluid">
  <div class="container">
      <h3>Warehouses</h3><br>

  {% for region in regions %}

      <div class="row">
                <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"> 
                  <a href="{% url 'fleet:insurance' %}">
                  <div class="info-box gray-bg">
                <a href="{% url 'fleet:region' region.id  %}" class="list-group-item list-group-item-action">{{ region.name }}</a>
                </a>
                </div>
                </div>     
      </div> 
      <div class="row">
          <!-- profile-widget -->
          <div class="col-lg-12">
            <div class="profile-widget profile-widget-info">
              <div class="panel-body">
                <div class="col-lg-2 col-sm-2">
                <a href="{% url 'fleet:region' region.id  %}">{{ region.name }}</a>
                  <div class="follow-ava">
                    <img src="img/profile-widget-avatar.jpg" alt="">
                  </div>
                  <h6>Administrator</h6>
                </div>
                <div class="col-lg-4 col-sm-4 follow-info">
                  <p>Hello I’m Jenifer Smith, a leading expert in interactive and creative design.</p>
                  <p>@jenifersmith</p>
                  <p><i class="fa fa-twitter">jenifertweet</i></p>

                </div>

                
                <div class="col-lg-2 col-sm-6 follow-info weather-category">
                  <ul>
                    <li class="active">

                      <i class="fa fa-tachometer fa-2x"> </i><br> Contrary to popular belief, Lorem 
                    </li>

                  </ul>
                </div>

                <div class="col-lg-2 col-sm-6 follow-info weather-category">
                  <ul>
                    <li class="active">

                      <i class="fa fa-bell fa-2x"> </i><br> Contrary to popular belief, Lorem 
                    </li>

                  </ul>
                </div>

              </div>
            </div>
          </div>
        </div> 
  {% endfor %}

  </div>
</div>

class Fleet(models.Model):

	vehmas_veh = models.CharField(max_length = 30, verbose_name = 'Vehicle number', unique = True)
	vehmas_size = models.CharField(max_length = 15, verbose_name= 'Vehicle size')
	vehmas_manfr = models.CharField(max_length = 25, verbose_name= 'Manufacturer')
	vehmas_model = models.CharField(max_length = 50, verbose_name= 'Model')
	vehmas_chno = models.CharField(max_length = 50, verbose_name= 'Chassis number', null = True, blank = True)
	vehmas_engno = models.CharField(max_length = 40, verbose_name= 'Engine number', null = True, blank = True)
	vehmas_reg = models.FileField(upload_to='media', null = True, blank = True, verbose_name= 'Registratrion file')
	vehmas_region = models.ForeignKey(Region, on_delete = models.CASCADE, null = True, blank = True)
	vehmas_btryno = models.CharField(max_length = 20, verbose_name = 'Battery code', null = True, blank = True)
	vehmas_btrymodel = models.CharField(max_length = 20, verbose_name = 'Battery Model', null = True, blank = True)
	vehmas_insno = models.CharField(max_length = 20, verbose_name= 'Insurance Policy number', null = True, blank = True)
	vehmas_insdate = models.DateField(verbose_name = 'Insurance expiry', null = True, blank = True)
	vehmas_insfile = models.FileField(default='', verbose_name = 'Insurance File', upload_to='media', null = True, blank = True)
	# insamt = models.IntegerField(verbose_name = 'Insurance amount', default = 0, null = True, blank = True)
	vehmas_taxno = models.CharField(max_length = 20, verbose_name= 'Tax number', null = True, blank = True)
	vehmas_taxdate = models.DateField(verbose_name= 'Tax Expiry', null = True, blank = True)
	vehmas_taxfile = models.FileField(default='', verbose_name = 'Tax File', upload_to='media', null = True, blank = True)
	vehmas_perno = models.CharField(max_length = 20, verbose_name= 'Permit number', null = True, blank = True)
	vehmas_perdate = models.DateField(verbose_name = 'Permit expiry', null = True, blank = True)
	vehmas_perfile = models.FileField(default='', verbose_name = 'Permit File', upload_to='media', null = True, blank = True)
	vehmas_fitnno = models.CharField(max_length = 20, verbose_name= 'Fitness number', null = True, blank = True)
	vehmas_fitndate = models.DateField(verbose_name= 'Fitness Expiry', null = True, blank = True)
	vehmas_fitnfile = models.FileField(default='', verbose_name = 'Fitness File', upload_to='media', null = True, blank = True)
	vehmas_polno = models.CharField(max_length = 20, verbose_name= 'Pollution number', null = True, blank = True)
	vehmas_poldate = models.DateField(verbose_name= 'Pollution Expiry', null = True, blank = True)
	vehmas_polfile = models.FileField(default='', verbose_name = 'Pollution File', upload_to='media', null = True, blank = True)
	vehmas_welfrno = models.CharField(max_length = 20, verbose_name= 'Welfare number', null = True, blank = True)
	vehmas_welfrdate = models.DateField(verbose_name= 'Welfare Expiry', null = True, blank = True)
	vehmas_welfrfile = models.FileField(default='', verbose_name = 'Welfare File', upload_to='media', null = True, blank = True)
	vehmas_acc = models.ManyToManyField('Accessories' , verbose_name = 'Accessories', blank = True)
	vehmas_other = models.CharField(max_length = 50, verbose_name = 'Other Accessories', null = True, blank = True)
	vehmas_tyreno = models.IntegerField(verbose_name = 'No. of Tyres', default = 4, null = True, blank = True)
	vehmas_driver = models.ForeignKey(Driver, on_delete = models.CASCADE, null = True, blank = True)
	vehmas_istatus = models.CharField(max_length = 50, null = True, blank = True)
	vehmas_tstatus = models.CharField(max_length = 40, null = True, blank = True)
	vehmas_pstatus = models.CharField(max_length = 40, null = True, blank = True)
	vehmas_fstatus = models.CharField(max_length = 40, null = True, blank = True)
	vehmas_postatus = models.CharField(max_length = 40, null = True, blank = True)
	vehmas_wstatus = models.CharField(max_length = 40, null = True, blank = True)
	# activity = models.TextField(blank = True, null = True, verbose_name = "Activity")


	def get_absolute_url(self):
		return reverse('fleet-update', kwargs={'pk': self.pk})

	def __str__(self):
		return str(self.veh)

	def save(self, *args, **kwargs):

		self.full_clean() # performs regular validation then clean()
		super(Fleet, self).save(*args, **kwargs)

	def clean(self):
		if self.veh:
			self.veh = self.veh.replace(" ","")

	class Meta:
		managed = True


from django import forms
from fleet.models import Tyre, Fleet, Accessories, Driver, Trip, FuelLog, Tripsheet
from django.forms import ModelForm, inlineformset_factory, ModelMultipleChoiceField
from django_select2.forms import ModelSelect2Widget
from dal import autocomplete


# class FleetForm(ModelForm):

# 	acc = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Accessories.objects.all())
# 	# acc = forms.ModelMultipleChoiceField(queryset=Accessories.objects.all(),widget=forms.CheckboxSelectMultiple(),required=True)	

# 	class Meta:
# 		model: Fleet
# 		exclude = ('driver',)

# 	def __init__(self, *args, **kwargs):

# 		super(FleetForm, self).__init__(*args, **kwargs)
# 		self.fields["acc"].widget = CheckboxSelectMultiple()
# 		self.fields["acc"].queryset = Accessories.objects.all()

class FuelLogForm(ModelForm):

	veh = forms.ModelChoiceField(queryset = Fleet.objects.all(), widget = autocomplete.ModelSelect2(url='veh-autocomp'))

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

class 	

class TyreForm(ModelForm):
    class Meta:
        model = Tyre
        exclude = ()

TyreFormSet = inlineformset_factory(Fleet, Tyre,
                                            form=TyreForm, extra=5)

class Tyre(ModelForm):

	class Meta:
		model = Tyre
		exclude = ('desc', 'flt')

TyreFormSet - inlineformset_factory(F)

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
    veh = forms.ModelChoiceField(queryset = Fleet.objects.all(), widget = autocomplete.ModelSelect2(url='veh-autocomp'))

    class Meta:
        model = Tripsheet
        fields = '__all__'

class TripForm(ModelForm):

	driver = forms.ModelChoiceField(queryset = Driver.objects.all(), widget = autocomplete.ModelSelect2(url='driver-autocomp'))
	veh = forms.ModelChoiceField(queryset = Fleet.objects.all(), widget = autocomplete.ModelSelect2(url='veh-autocomp'))

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

