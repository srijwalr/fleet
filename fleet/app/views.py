from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from app.models import Vehiclemaster, Tyre, FuelLog, Driver, Region, Trip, Tripsheet
from django.urls import reverse_lazy
from django.contrib import auth
from django.urls import reverse_lazy, reverse
from django.contrib.auth import (authenticate, login, logout, update_session_auth_hash)
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       PasswordChangeForm)
from django.http import HttpResponseRedirect                                       
from .forms import TyreFormSet, PDriverForm,TDriverForm, TripstartForm, TripendForm, FuelLogForm, ExpenseForm, TripsheetForm, ProfileCreationForm
from django.db import transaction
from datetime import datetime, timezone
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import urllib.request, json
from dal import autocomplete
# import viewsets 
from django.views.generic import View
# from rest_framework import viewsets 

# import local data 
# from .serializers import FleetSerializer , TripsheetSerializers, DriverSerializers
from .models import Vehiclemaster

from django.template.loader import get_template
from . import utils

from django.db.models import Sum
from slick_reporting.views import SlickReportView



class LogoutView(View):
    def get(self, request):
        logout(request)
        form = ProfileCreationForm(self.request.POST or None)
        context = {
            "form": form,
        }
        return render(self.request, 'login.html', context)


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect(
                        reverse('app:fleet')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )   
    return render(request, 'login.html', {'form': form})

# class TripsheetViewSet(viewsets.ModelViewSet):
#     queryset = Tripsheet.objects.all()
#     serializer_class = TripsheetSerializers
# create a viewset 
# class FleetViewSet(viewsets.ModelViewSet): 
#     # define queryset 
#     queryset = Vehiclemaster.objects.all() 
    
#     # specify serializer to be used 
#     serializer_class = VehiclemasterSerializer 


# class DriverViewSet(viewsets.ModelViewSet):
#     queryset = Driver.objects.all()
#     serializer_class = DriverSerializers

class DriverAutocomp(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Driver.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

class VehAutocomp(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        qs = Vehiclemaster.objects.all()
        if self.q:
            qs = qs.filter(veh__istartswith=self.q)
        return qs

def Tripgen(request):
    if request.method=='POST':
        billno=request.POST.get('LrTran_waybillno')
        km=request.POST.get('LrTran_Km')
        kmrate=request.POST.get('LrTran_Kmrate')
        driver=request.POST.get('LrTran_DriverDtls')
        frtbillno=request.POST.get('LrTran_Frtypebillno')
        data=Trip.objects.create(billno=billno,km=km,kmrate=kmrate,driver=driver,frtbillno=frtbillno)
        return HttpResponseRedirect(reverse('detail'))
    return render(request,"app/tripgen.html ",{})

def detail(request):
    #data=offer.objects.all()
    url = "http://13.71.87.214:88/api/Lrtransation"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    return render(request,"app/detail.html",{'data':data})


@login_required(login_url='/signin')
def fleetlist(request):
    object_list = Vehiclemaster.objects.filter(vehmas_frtyppntr = 6)

    query = request.GET.get("q")
    if query:
        object_list = object_list.filter(
            Q(vehmas_code__icontains=query) |
                Q(region__name__icontains=query)
            ).distinct()
        
        return render(request, 'app/fleet_list.html', {
            'object_list': object_list,
        })
    else:
        page = request.GET.get('page', 1)

        paginator = Paginator(object_list, 10)
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)

        return render(request, 'app/fleet_list.html', {'object_list': object_list}) 

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class FleetDetailView(DetailView):
    model = Vehiclemaster
    template_name = "app/fltdetail.html"

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class DriverDetailView(DetailView):
    model = Driver
    template_name = "app/drvr_detail.html"


@method_decorator(login_required(login_url='/signin'), name='dispatch')    
class FleetCreate(CreateView):
    model = Vehiclemaster
    # fields = '__all__'
    fields = ('vehmas_desc','size','manfr','model','chno','engno','reg','region','btryno','btrymodel','insno','insdate','insfile','taxno','taxdate','taxfile','perno','perdate','perfile','fitnno','fitndate','fitnfile','polno','poldate','polfile','welfrno','welfrdate','welfrfile','acc','other','tyreno',)  
    success_url = reverse_lazy('app:fleet-list')

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class FleetTyreCreate(CreateView):
    model = Vehiclemaster
    fields = ('vehmas_desc','size','manfr','model','chno','engno','reg','region','btryno','btrymodel','insno','insdate','insfile','taxno','taxdate','taxfile','perno','perdate','perfile','fitnno','fitndate','fitnfile','polno','poldate','polfile','welfrno','welfrdate','welfrfile','acc','other','tyreno',)  
    success_url = reverse_lazy('app:fleet-list')

    def get_context_data(self, **kwargs):
        data = super(FleetTyreCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['tyres'] = TyreFormSet(self.request.POST)
        else:
            data['tyres'] = TyreFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        tyres = context['tyres']
        with transaction.atomic():
            self.object = form.save()

            if tyres.is_valid():
                tyres.instance = self.object
                tyres.save()
        return super(FleetTyreCreate, self).form_valid(form)


@method_decorator(login_required(login_url='/signin'), name='dispatch')
class FleetUpdate(UpdateView):
    model = Vehiclemaster
    success_url = reverse_lazy('app:fleet-list')
    fields = '__all__'


@method_decorator(login_required(login_url='/signin'), name='dispatch')
class FleetTyreUpdate(UpdateView):
    model = Vehiclemaster
    fields = ('size','manfr','model','chno','engno','reg','region','btryno','btrymodel','insno','insdate','insfile','taxno','taxdate','taxfile','perno','perdate','perfile','fitnno','fitndate','fitnfile','polno','poldate','polfile','welfrno','welfrdate','welfrfile','acc','other','tyreno',)
    success_url = reverse_lazy('app:fleet-list')

    def get_context_data(self, **kwargs):
        data = super(FleetTyreUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['tyres'] = TyreFormSet(self.request.POST, instance=self.object)
        else:
            data['tyres'] = TyreFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        tyres = context['tyres']
        with transaction.atomic():
            self.object = form.save()

            if tyres.is_valid():
                tyres.instance = self.object
                tyres.save()
        return super(FleetTyreUpdate, self).form_valid(form)



@method_decorator(login_required(login_url='/signin'), name='dispatch')
class DriverAllocate(UpdateView):

    model = Vehiclemaster
    fields = ('driver',)
    template_name = 'app/allocate.html'
    success_url = reverse_lazy('app:fleet-list')

    def get_context_data(self, **kwargs):

        context = super(DriverAllocate, self).get_context_data(**kwargs)
        context['driver'] = Vehiclemaster.objects.filter(veh=self.object)
        return context

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class FleetDelete(DeleteView):
    model = Vehiclemaster
    success_url = reverse_lazy('app:fleet-list')

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class FuelLogAdd(CreateView):
    model = FuelLog
    form_class = FuelLogForm
    template_name = 'app/fuellog.html'
    success_url = reverse_lazy('app:logs')
    # fields = ('veh','size','manfr','driver','no','date','diesel','petrol','lub','othr','odo','fuel')

@login_required(login_url='/signin')
def loglist(request):
    try:

        start_date = request.POST.get('start_date')
        stop_date = request.POST.get('stop_date')
        object_list = FuelLog.objects.all()
        object_list = object_list.filter(date__range=[start_date, stop_date])
        # print(object_list)
        return render(request, 'app/logresult.html', {
            'object_list': object_list,
        })
    except:
        return render(request, 'app/loglist.html', {'error_message': 'Enter dates'})

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class FuelLogView(ListView):
    model = FuelLog
    template_name = 'app/loglist.html'
    queryset = FuelLog.objects.all()
    context_object_name = 'fuellogs'  
    paginate_by = 10

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class LogDetailView(DetailView):
    model = FuelLog
    template_name = "app/logdetail.html"

@login_required(login_url='/signin')
def region_data(request,**kwargs):
    if not request.user.is_authenticated:
        return render(request, 'sign_in.html')
    else:
        id = kwargs['region_id']
        region = Region.objects.filter(id=id).first()
        result = Vehiclemaster.objects.filter(region = region, vehmas_frtyppntr = 6)
        page = request.GET.get('page', 1)

        paginator = Paginator(result, 10)
        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)
        return render(request, 'app/region-list.html', {
            'fleetlist': result,
        })            

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class FleetView(ListView):
    model = Vehiclemaster
    template_name = "app/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        querydata = Vehiclemaster.objects.filter( vehmas_frtyppntr = 6)
        objectlist1 = []
        objectlist2 = []
        objectlist3 = []
        objectlist4 = []
        objectlist5 = []
        objectlist6 = []
        for q in querydata:
            try:
                k = q.insdate - datetime.now().date()
                l = q.taxdate - datetime.now().date()
                m = q.perdate - datetime.now().date()
                n = q.fitndate - datetime.now().date()
                p = q.poldate - datetime.now().date()
                r = q.welfrdate - datetime.now().date()
                if k.days > 30:
                    istatus="scheduled"
                if k.days <= 30:
                    istatus="duesoon"
                    objectlist1.append(q)
                if k.days < 0:
                    istatus="overdue"

                if l.days > 30:
                    tstatus="scheduled"
                if l.days <= 30:
                    tstatus="duesoon"
                    objectlist2.append(q)
                if l.days < 0:
                    tstatus="overdue"

                if m.days > 30:
                    pstatus="scheduled"
                if m.days <= 30:
                    pstatus="duesoon"
                    objectlist3.append(q)
                if m.days < 0:
                    pstatus="overdue"

                if n.days > 30:
                    fstatus="scheduled"
                if n.days <= 30:
                    fstatus="duesoon"
                    objectlist4.append(q)
                if n.days < 0:
                    fstatus="overdue"

                if p.days > 30:
                    postatus="scheduled"
                if p.days <= 30:
                    postatus="duesoon"
                    objectlist5.append(q)
                if p.days < 0:
                    postatus="overdue"

                if r.days > 30:
                    wstatus="scheduled"
                if r.days <= 30:
                    wstatus="duesoon"
                    objectlist6.append(q)
                if r.days < 0:
                    wstatus="overdue"

                q.istatus = istatus
                q.tstatus = tstatus
                q.pstatus = pstatus
                q.fstatus = fstatus
                q.postatus = postatus
                q.wstatus = wstatus
            except:
                objectlist1 = []
                objectlist2 = []
                objectlist3 = []
                objectlist4 = []
                objectlist5 = []
                objectlist6 = []
        # count = Vehiclemaster.objects.filter(status='').aggregate(Count('veh'))
        regions = Region.objects.all()
        context['reminders1'] = objectlist1
        context['reminders2'] = objectlist2
        context['reminders3'] = objectlist3
        context['reminders4'] = objectlist4
        context['reminders5'] = objectlist5
        context['reminders6'] = objectlist6
        context['regions'] = regions
        # context['count'] = count

        return context

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class InsView(ListView):
    model = Vehiclemaster
    template_name = "app/insrem.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        querydata = Vehiclemaster.objects.all()
        objectlist1 = []
        for q in querydata:
            k = q.insdate - datetime.now().date()
            if k.days > 30:
                istatus="scheduled"
            if k.days <= 30:
                istatus="duesoon"
                objectlist1.append(q)
            if k.days < 0:
                istatus="overdue"
            q.istatus = istatus
        context['reminders1'] = objectlist1
        return context

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class TaxView(ListView):
    model = Vehiclemaster
    template_name = "app/taxrem.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        querydata = Vehiclemaster.objects.all()
        objectlist2 = []
        for q in querydata:
            l = q.taxdate - datetime.now().date()
            if l.days > 30:
                tstatus="scheduled"
            if l.days <= 30:
                tstatus="duesoon"
                objectlist2.append(q)
            if l.days < 0:
                tstatus="overdue"
            q.tstatus = tstatus
        context['reminders2'] = objectlist2
        return context

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class PermitView(ListView):
    model = Vehiclemaster
    template_name = "app/perrem.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        querydata = Vehiclemaster.objects.all()
        objectlist3 = []
        for q in querydata:
            m = q.perdate - datetime.now().date()
            if m.days > 30:
                pstatus="scheduled"
            if m.days <= 30:
                pstatus="duesoon"
                objectlist3.append(q)
            if m.days < 0:
                pstatus="overdue"
            q.pstatus = pstatus
        context['reminders3'] = objectlist3
        return context

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class FitnessView(ListView):
    model = Vehiclemaster
    template_name = "app/fitrem.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        querydata = Vehiclemaster.objects.all()
        objectlist4 = []
        for q in querydata:
            n = q.fitndate - datetime.now().date()
            if n.days > 30:
                fstatus="scheduled"
            if n.days <= 30:
                fstatus="duesoon"
                objectlist4.append(q)
            if n.days < 0:
                fstatus="overdue"
            q.fstatus = fstatus
        context['reminders4'] = objectlist4
        return context

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class PollutionView(ListView):
    model = Vehiclemaster
    template_name = "app/polrem.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        querydata = Vehiclemaster.objects.all()
        objectlist5 = []
        for q in querydata:
            p = q.poldate - datetime.now().date()
            if p.days > 30:
                postatus="scheduled"
            if p.days <= 30:
                postatus="duesoon"
                objectlist5.append(q)
            if p.days < 0:
                postatus="overdue"
            q.postatus = postatus
        context['reminders5'] = objectlist5
        return context

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class WelfareView(ListView):
    model = Vehiclemaster
    template_name = "app/welrem.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        querydata = Vehiclemaster.objects.all()
        objectlist6 = []
        for q in querydata:
            r = q.welfrdate - datetime.now().date()
            if r.days > 30:
                wstatus="scheduled"
            if r.days <= 30:
                wstatus="duesoon"
                objectlist6.append(q)
            if r.days < 0:
                wstatus="overdue"
            q.wstatus = wstatus
        context['reminders6'] = objectlist6
        return context

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'sign_in.html')
    else:
        regions = Region.objects.all()

        return render(request, 'app/msfleet.html', {'regions': regions})

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class TripsheetCreate(CreateView):
    model = Tripsheet
    form_class = TripsheetForm
    template_name = 'app/tripsheet.html'
    success_url = reverse_lazy('app:triplog')

# @method_decorator(login_required(login_url='/signin'), name='dispatch')
# class TripCreate(CreateView):
#     model = Trip
#     form_class = TripForm
#     template_name = 'app/trip_form.html'
#     success_url = reverse_lazy('app:trip-list')
#     # fields = ('no','driver','veh','ftype','start','end','source','dest','region','lr','date')


@method_decorator(login_required(login_url='/signin'), name='dispatch')
class TripUpdate(UpdateView):
    model = Trip
    success_url = reverse_lazy('app:trip-list')
    fields = ('no','driver','veh','ftype','start','end','km','source','dest','region','lr','date','is_approved')

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class TripList(ListView):
    model = Trip
    template_name = 'app/trip_list.html'
    queryset = Trip.objects.all()
    context_object_name = 'trips'  
    paginate_by = 10


@method_decorator(login_required(login_url='/signin'), name='dispatch')
class TripsheetList(ListView):
    model = Tripsheet
    template_name = 'app/triplog.html'
    queryset = Tripsheet.objects.all()
    context_object_name = 'tripsheet'  
    paginate_by = 10


@login_required(login_url='/signin')
def trips(request, filter_by):

    trips = Trip.objects.all()
    if filter_by == 'approved':
        trips = Trip.objects.filter(is_approved=False)
    
    page = request.GET.get('page', 1)

    paginator = Paginator(trips, 10)
    try:
        trips = paginator.page(page)
    except PageNotAnInteger:
        trips = paginator.page(1)
    except EmptyPage:
        trips = paginator.page(paginator.num_pages)


    return render(request, 'app/trips.html', {
        'trip_list': trips,
        'filter_by': filter_by,
    })


@method_decorator(login_required(login_url='/signin'), name='dispatch')
class PDriverCreate(CreateView):
    model = Driver
    form_class = PDriverForm
    success_url = reverse_lazy('app:driver-list')
    # fields = '__all__'

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class TDriverCreate(CreateView):
    model = Driver
    form_class = TDriverForm
    success_url = reverse_lazy('app:driver-list')
    # fields = '__all__'

@method_decorator(login_required(login_url='/signin'), name='dispatch')
class DriverExpense(UpdateView):
    model = Driver
    form_class = ExpenseForm
    success_url = reverse_lazy('app:driver-list')


@method_decorator(login_required(login_url='/signin'), name='dispatch')
class DriverUpdate(UpdateView):
    model = Driver
    success_url = reverse_lazy('app:driver-list')
    fields = ('name','bata','is_settled')


@method_decorator(login_required(login_url='/signin'), name='dispatch')
class DriverList(ListView):
    model = Driver
    template_name = 'app/driver_list.html'
    queryset = Driver.objects.all()
    context_object_name = 'drivers'  
    paginate_by = 10


@method_decorator(login_required(login_url='/signin'), name='dispatch')
class Salaryreport(ListView):
    model = Driver
    template_name = 'app/salaryrprt.html'
    queryset = Driver.objects.all()
    context_object_name = 'drivers'  
    paginate_by = 10


@login_required(login_url='/signin')
def salary(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="salary_report.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Driver')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['NAME', 'BATA', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Driver.objects.all().values_list('name', 'bata')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

@login_required(login_url='/signin')
def gettrip(request):
    # object_list = Trip.objects.all()

    query = request.GET.get("q")
    if query:
        result = get_object_or_404(Trip, tripno = query)
        # result = object_list.get(
        #     Q(tripno__icontains=query))
        if result.start > 0:
            form = TripendForm(request.POST or None, instance=result)
            if form.is_valid(): 
                form.save() 
                return HttpResponseRedirect("/fleet") 
        else:
            form = TripstartForm(request.POST or None, instance=result)
            if form.is_valid(): 
                form.save() 
                return HttpResponseRedirect("/fleet")             
            
        return render(request, 'app/gettrip.html', {
            'form': form,
        })
    else:
        pass


@login_required(login_url='/signin')
def entry(request):
    # object_list = Trip.objects.all()

    query = request.GET.get("q")
    if query:
        query = query.replace(" ","")
        query = query.upper()

            
        try:            
            result = Fleet.objects.get(veh = query)
        except:
            EntryTable.objects.create(veh = query, in_time = datetime.now(), purpose = 'New vehicle')
            return render(request, 'app/msfleet.html', {'error_message': 'New vehicle entry noted'})


        trip = Trip.objects.filter(veh = result).first()
        if result.status == 4:                                                  #on trip
            if trip.start > 0:
                form = TripendForm(request.POST or None, instance=trip)
                if form.is_valid(): 
                    form.save() 
                    result.status = 1   
                    result.save()                                                    #available
                    EntryTable.objects.create(veh = result, in_time = datetime.now(), purpose = 'In after trip')
                    return HttpResponseRedirect("/fleet")             


            return render(request, 'app/gettrip.html', {
                'form': form,
                'trip': trip,
            })

        elif result.status == 3:                                                #trip assigned
            # if result.start == 0:
            form = TripstartForm(request.POST or None, instance=trip)
            if form.is_valid(): 
                form.save() 
                result.status = 4      
                result.save()                                                   #on trip
                EntryTable.objects.create(veh = result, out_time = datetime.now(), purpose = 'Out for delivery')
                return HttpResponseRedirect("/fleet")     
                            
            return render(request, 'app/gettrip.html', {
                'form': form,
                'trip': trip,
            })

        elif result.status == 2:                                                 #outside
            result.status = 1
            result.save()
            EntryTable.objects.create(veh = result, in_time = datetime.now(), purpose = 'In without load')
            return render(request, 'app/fleetstatus.html', {'fleet': result})

        elif result.status == 1:                                                 #available
            result.status = 2
            result.save()
            EntryTable.objects.create(veh = result, out_time = datetime.now(), purpose = 'Out without load')
            return render(request, 'app/fleetstatus.html', {'fleet': result})

    else:
        return render(request, 'app/msfleet.html', {'error_message': 'Enter a vehicle number'})   

# @method_decorator(login_required(login_url='/signin'), name='dispatch')
# class EmiCreate(CreateView):
#     model = Emi
#     fields = '__all__'