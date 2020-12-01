from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import F    
from django.contrib.auth.models import AbstractUser

# Create your models here.
<<<<<<< HEAD
class Usercat(models.Model):
    id = models.IntegerField(primary_key = True, default = 1)
    code = models.CharField(max_length=4, blank=True, null=True)
    desc = models.CharField(max_length=20, blank=True, null=True)
    remarks = models.CharField(max_length=250, blank=True, null=True)
    active = models.CharField(max_length=1, blank=True, null=True)
    slno = models.IntegerField(blank=True, null=True)


    class Meta:
        db_table = 'UserCat'
  
    def __str__(self):
        return str(self.desc)

class Region(models.Model):
    name = models.CharField(max_length = 25, verbose_name = 'Region')
    image = models.ImageField(upload_to = 'media', null = True, blank = True)
    desc = models.CharField(max_length=30, verbose_name= 'Description')
    location = models.CharField(max_length = 25, verbose_name = "Location", null = True, blank = True)
    # location = models.PointField(
 #        "Location in Map", geography=True, blank=True, null=True,
 #        srid=4326,default='POINT(0.0 0.0)', help_text="Point(longitude latitude)")

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table  = 'Region'
        managed = True
    
    

class Profile(AbstractUser): 
    # usrd_id = models.AutoField(primary_key = True)
    usrcatpntr = models.ForeignKey(Usercat,null = True, blank = True, verbose_name= 'User Type', on_delete = models.CASCADE)
    code = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, verbose_name='Employee name', unique=True)
    # password = models.CharField(max_length=256, blank=True, null=True)
    slno = models.IntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=250, blank=True, null=True)
    active = models.CharField(max_length=1, verbose_name='User Status', blank=True, null=True)
    makerid = models.IntegerField(blank=True, null=True)
    maketime = models.DateTimeField(blank=True, null=True)
    logcount = models.IntegerField(blank=True, null=True)
    logattempt = models.IntegerField(blank=True, null=True)
    region = models.ForeignKey(Region, default = 1, db_column = 'region_id', on_delete = models.CASCADE, null = True, blank = True, verbose_name = "Region")
    
    # USERNAME_FIELD = 'name'
    class Meta:
        db_table = 'Profile'
=======
class Usercategory(models.Model):
    usrcat_id = models.IntegerField(primary_key = True, default = 1)
    usrcat_code = models.CharField(max_length=4, blank=True, null=True)
    usercat_desc = models.CharField(max_length=20, blank=True, null=True)
    usercat_remarks = models.CharField(max_length=250, blank=True, null=True)
    usercat_active = models.CharField(max_length=1, blank=True, null=True)
    usercat_slno = models.IntegerField(blank=True, null=True)


    class Meta:
        db_table = 'UserCategory'
  
    def __str__(self):
        return str(self.usercat_desc)

class Region(models.Model):
	name = models.CharField(max_length = 25, verbose_name = 'Region')
	image = models.ImageField(upload_to = 'media', null = True, blank = True)
	location = models.CharField(max_length = 25, verbose_name = "Location", null = True, blank = True)
	# location = models.PointField(
 #        "Location in Map", geography=True, blank=True, null=True,
 #        srid=4326,default='POINT(0.0 0.0)', help_text="Point(longitude latitude)")

	def __str__(self):
		return str(self.name)

class Profile(AbstractUser): 
    # usrd_id = models.AutoField(primary_key = True)
    usrcatpntr = models.ForeignKey(Usercategory,null = True, blank = True, verbose_name= 'User Type', on_delete = models.CASCADE)
    code = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, verbose_name='Employee name', unique=True, blank=True, null=True)
    password = models.CharField(max_length=256, blank=True, null=True)
    slno = models.IntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=250, blank=True, null=True)
    active = models.CharField(max_length=1, verbose_name='User Status', blank=True, null=True)
    makerid = models.IntegerField(blank=True, null=True)
    maketime = models.DateTimeField(blank=True, null=True)
    logcount = models.IntegerField(blank=True, null=True)
    logattempt = models.IntegerField(blank=True, null=True)
    region = models.ForeignKey(Region, on_delete = models.CASCADE, null = True, blank = True, verbose_name = "Region")
    
    # USERNAME_FIELD = 'name'
    # class Meta:
    #     db_table = 'userdetails'
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b

    def __str__(self):
        return str(self.username)



class Vehiclecategory(models.Model):
    vehcat_id = models.IntegerField(primary_key = True, default = 1)
    vehcat_code = models.CharField(max_length=50,verbose_name='Code', blank=True, null=True)
    vehcat_desc = models.CharField(max_length=100,verbose_name='Description', blank=True, null=True)
    vehcat_wtcapacity = models.FloatField(verbose_name='Weight capacity', blank=True, null=True)
    vehcat_length = models.FloatField(verbose_name='Length', blank=True, null=True)
    vehcat_width = models.FloatField(verbose_name='Width', blank=True, null=True)
    vehcat_ft = models.CharField(max_length=50, blank=True, null=True)
    vehcat_kmrate = models.DecimalField(max_digits=18, verbose_name='KM Rate', decimal_places=2, blank=True, null=True)
    vehcat_slno = models.IntegerField(verbose_name='Serial no.', blank=True, null=True)
    vehcat_active = models.CharField(max_length=1, blank=True, null=True)
    vehcat_remarks = models.CharField(max_length=250,verbose_name='Remarks', blank=True, null=True)
    vehcat_makerid = models.IntegerField(blank=True, null=True)
    vehcat_maketime = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.vehcat_code
    class Meta:
<<<<<<< HEAD
        managed = False
        # db_table = 'VehicleCategory'
=======
        db_table = 'VehicleCategory'
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b
  
class Freighttypes(models.Model):
    fretype_id = models.IntegerField(primary_key = True,default = 1)
    fretype_code = models.CharField(max_length=50,verbose_name='Code', blank=True, null=True)
    fretype_desc = models.CharField(max_length=100,verbose_name='Description', blank=True, null=True)
    fretype_slno = models.IntegerField(verbose_name='Serial no.', blank=True, null=True)
    fretype_remarks = models.CharField(max_length=250,verbose_name='Remarks', blank=True, null=True)
    fretype_active = models.CharField(max_length=1,verbose_name='Status', blank=True, null=True)
    fretype_nnc_code = models.CharField(max_length=10, blank=True, null=True)
    fretype_whmcode = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.fretype_desc
    class Meta:
        db_table = 'Freighttypes'
<<<<<<< HEAD
        # managed = False
     
class Accessories(models.Model):
    name = models.CharField(max_length = 25)

    def __str__(self):
        return str(self.name)

class Vehiclemaster(models.Model):

    FUELTYPE_CHOICES = (
        ('D', 'Diesel'),
        ('P', 'Petrol'),
        ('E', 'Electric'),
    )

    STATUS_CHOICES = (
        (1, 'Available'),
        (2, 'Unavailable'),
        (3, 'Trip assigned'),
        (4, 'On trip'),
        (5, 'Loading'),
        (6, 'Unloading'),
    )

    vehmas_id = models.IntegerField(primary_key = True, default = 1)
    vehmas_code = models.CharField(max_length=50,verbose_name='Vehicle Number')
    vehmas_desc = models.CharField(max_length=100,verbose_name='Description', blank=True, null=True)
    vehmas_catpntr = models.ForeignKey(Vehiclecategory, db_column = 'vehcat_id',verbose_name='Category',  on_delete = models.DO_NOTHING)
    vehmas_catpntr = models.IntegerField(verbose_name='Category',blank=True, null=True)
=======
 	
class Accessories(models.Model):
	name = models.CharField(max_length = 25)

	def __str__(self):
		return str(self.name)

class Vehiclemaster(models.Model):
    vehmas_id = models.IntegerField(primary_key = True, default = 1)
    vehmas_code = models.CharField(max_length=50,verbose_name='Vehicle Number', blank=True, null=True)
    vehmas_desc = models.CharField(max_length=100,verbose_name='Description', blank=True, null=True)
    vehmas_catpntr = models.ForeignKey(Vehiclecategory, db_column = 'vehcat_id',verbose_name='Category',  on_delete = models.DO_NOTHING)
    # vehmas_catpntr = models.IntegerField(verbose_name='Category',blank=True, null=True)
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b
    vehmas_drivername = models.CharField(max_length= 20, verbose_name= 'Driver Name', blank=True, null = True)
    vehmas_driverphone = models.CharField(max_length= 15,verbose_name='Phone Number', blank=True, null=True )
    vehmas_frtyppntr = models.ForeignKey(Freighttypes,db_column = 'fretype_id', verbose_name='Vehicle Mode', blank=True, null=True, on_delete = models.DO_NOTHING)
    # vehmas_frtyppntr = models.IntegerField(verbose_name='Vehicle Mode', blank=True, null=True)
    vehmas_modepntr = models.IntegerField(blank=True, null=True)
    # vehmas_slno = models.IntegerField(blank=True, null=True)
    vehmas_active = models.CharField(max_length=1,verbose_name='Status', blank=True, null=True)
    # vehmas_remarks = models.CharField(max_length=250, blank=True, null=True)
    vehmas_makerid = models.IntegerField(blank=True, null=True)
<<<<<<< HEAD
    vehmas_maketime = models.CharField(blank=True, null=True, max_length = 30)
    vehmas_clntpntr = models.IntegerField(blank=True, null=True)

    size = models.CharField(max_length = 15, verbose_name= 'Vehicle size')
    manfr = models.CharField(max_length = 25, verbose_name= 'Manufacturer')
    model = models.CharField(max_length = 50, verbose_name= 'Model')
    ftype = models.CharField(max_length = 10, verbose_name= 'Fuel type', default='D', choices= FUELTYPE_CHOICES)
=======
    vehmas_maketime = models.DateTimeField(blank=True, null=True)
    vehmas_clntpntr = models.IntegerField(blank=True, null=True)

    # veh = models.CharField(max_length = 30, verbose_name = 'Vehicle number')
    size = models.CharField(max_length = 15, verbose_name= 'Vehicle size')
    manfr = models.CharField(max_length = 25, verbose_name= 'Manufacturer')
    model = models.CharField(max_length = 50, verbose_name= 'Model')
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b
    chno = models.CharField(max_length = 50, verbose_name= 'Chassis number', null = True, blank = True)
    engno = models.CharField(max_length = 40, verbose_name= 'Engine number', null = True, blank = True)
    reg = models.FileField(upload_to='media', null = True, blank = True, verbose_name= 'Registratrion file')
    region = models.ForeignKey(Region, on_delete = models.CASCADE, null = True, blank = True)
    btryno = models.CharField(max_length = 20, verbose_name = 'Battery code', null = True, blank = True)
    btrymodel = models.CharField(max_length = 20, verbose_name = 'Battery Model', null = True, blank = True)
    insno = models.CharField(max_length = 20, verbose_name= 'Insurance Policy number', null = True, blank = True)
    insdate = models.DateField(verbose_name = 'Insurance expiry', null = True, blank = True)
    insfile = models.FileField(default='', verbose_name = 'Insurance File', upload_to='media', null = True, blank = True)
<<<<<<< HEAD
    insamt = models.IntegerField(verbose_name = 'Insurance amount', default = 0, null = True, blank = True)
=======
	# insamt = models.IntegerField(verbose_name = 'Insurance amount', default = 0, null = True, blank = True)
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b
    taxno = models.CharField(max_length = 20, verbose_name= 'Tax number', null = True, blank = True)
    taxdate = models.DateField(verbose_name= 'Tax Expiry', null = True, blank = True)
    taxfile = models.FileField(default='', verbose_name = 'Tax File', upload_to='media', null = True, blank = True)
    perno = models.CharField(max_length = 20, verbose_name= 'Permit number', null = True, blank = True)
    perdate = models.DateField(verbose_name = 'Permit expiry', null = True, blank = True)
    perfile = models.FileField(default='', verbose_name = 'Permit File', upload_to='media', null = True, blank = True)
    fitnno = models.CharField(max_length = 20, verbose_name= 'Fitness number', null = True, blank = True)
    fitndate = models.DateField(verbose_name= 'Fitness Expiry', null = True, blank = True)
    fitnfile = models.FileField(default='', verbose_name = 'Fitness File', upload_to='media', null = True, blank = True)
    polno = models.CharField(max_length = 20, verbose_name= 'Pollution number', null = True, blank = True)
    poldate = models.DateField(verbose_name= 'Pollution Expiry', null = True, blank = True)
    polfile = models.FileField(default='', verbose_name = 'Pollution File', upload_to='media', null = True, blank = True)
    welfrno = models.CharField(max_length = 20, verbose_name= 'Welfare number', null = True, blank = True)
    welfrdate = models.DateField(verbose_name= 'Welfare Expiry', null = True, blank = True)
    welfrfile = models.FileField(default='', verbose_name = 'Welfare File', upload_to='media', null = True, blank = True)
    acc = models.ManyToManyField('Accessories' , verbose_name = 'Accessories', blank = True)
    other = models.CharField(max_length = 50, verbose_name = 'Other Accessories', null = True, blank = True)
    tyreno = models.IntegerField(verbose_name = 'No. of Tyres', default = 4, null = True, blank = True)
<<<<<<< HEAD
    # driver = models.ForeignKey(Driver, on_delete = models.CASCADE, null = True, blank = True)
=======
	# driver = models.ForeignKey(Driver, on_delete = models.CASCADE, null = True, blank = True)
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b
    istatus = models.CharField(max_length = 50, null = True, blank = True)
    tstatus = models.CharField(max_length = 40, null = True, blank = True)
    pstatus = models.CharField(max_length = 40, null = True, blank = True)
    fstatus = models.CharField(max_length = 40, null = True, blank = True)
    postatus = models.CharField(max_length = 40, null = True, blank = True)
    wstatus = models.CharField(max_length = 40, null = True, blank = True)
<<<<<<< HEAD
    odo = models.IntegerField(verbose_name = 'Odo reading', default = 0, null = True, blank = True)
    status = models.IntegerField(verbose_name= 'Vehicle status', default=2,  choices= STATUS_CHOICES)
    activity = models.TextField(blank = True, null = True, verbose_name = "Activity")
=======
	# activity = models.TextField(blank = True, null = True, verbose_name = "Activity")
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b


    def get_absolute_url(self):
        return reverse('fleet-update', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):

        self.full_clean() # performs regular validation then clean()
        super(Vehiclemaster, self).save(*args, **kwargs)

    def clean(self):
        if self.vehmas_desc:
            self.vehmas_desc = self.vehmas_desc.replace(" ","")
<<<<<<< HEAD
            self.vehmas_desc = self.vehmas_desc.upper()

=======
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b

    def __str__(self):
        return str(self.vehmas_code)
    class Meta:
<<<<<<< HEAD
            # managed = False
        db_table = 'VehicleMaster'


class Maintenance(models.Model):

    veh = models.ForeignKey(Vehiclemaster, verbose_name='Vehicle', on_delete = models.DO_NOTHING)
    head = models.CharField(max_length= 30, verbose_name= 'Purpose')
    cost = models.IntegerField(default= 0, verbose_name= 'Cost')
    narration = models.TextField(verbose_name= 'Narration')
    timestamp = models.DateField(default=datetime.now, verbose_name= "Time")

=======
        db_table = 'VehicleMaster'


>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b
class Tyre(models.Model):

    DESC_CHOICES = (
        ('FL', 'Front Left'),
        ('FR', 'Front Right'),
        ('BL', 'Back Left'),
        ('BR', 'Back Right'),
        ('BL1', 'Back Left+1'),
        ('BR1', 'Back Right+1'),
        ('ST', 'Stepney'),
        ('OT', 'Others'),
    )

    flt = models.ForeignKey(Vehiclemaster, db_column = 'vehmas_id', verbose_name='Vehicle', blank=True, null=True, on_delete = models.DO_NOTHING)
    desc = models.CharField(max_length = 7, verbose_name = 'Description', choices = DESC_CHOICES)
    dtl = models.CharField(max_length = 15, verbose_name = 'Tyre no.')
    make = models.CharField(max_length = 25,verbose_name = 'Make')

<<<<<<< HEAD

    def __str__(self):
        return str(self.dtl)

    class Meta:
        db_table = 'Tyre'
=======
    class Meta:
        # managed = True
        db_table = 'Tyre'

    def __str__(self):
        return str(self.dtl)
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b
    


class Driver(models.Model):

<<<<<<< HEAD
    # code = models.CharField(max_length = 10, verbose_name = "Driver ID")
    name = models.CharField(max_length = 30, verbose_name = 'Driver name', unique = True)
    phone = models.CharField(max_length = 12, verbose_name = 'Phone number')
    region = models.ForeignKey(Region, on_delete = models.CASCADE, verbose_name = 'Region')
    bata = models.IntegerField(null = True, blank = True, default = 0, verbose_name = "BATA")
    advance = models.IntegerField(default = 0, verbose_name = "Advance")
    expense = models.IntegerField(default = 0, verbose_name = "Expense")
    is_settled = models.BooleanField(default = False, verbose_name = "Salary settlement")
    # activity = models.TextField(blank = True, null = True, verbose_name = "Activity")
    address = models.TextField(blank = True, null = True, verbose_name = "Address")
    salary = models.IntegerField(default = 0, verbose_name = "Fixed salary")
    photo = models.ImageField(upload_to = 'media', null = True, blank = True)
    licence = models.FileField(upload_to = 'media', null = True, blank = True)
    lno = models.CharField(max_length= 16, verbose_name= 'Licence number')
    lexpiry = models.DateField(verbose_name= "License expiry", null = True, blank = True)
    rationcard = models.FileField(upload_to = 'media', null = True, blank = True)
    aadhar = models.FileField(upload_to = 'media', null = True, blank = True)
    is_temp = models.BooleanField(default = False, verbose_name = "Permanent")
    payment = models.IntegerField(default = 0, verbose_name = "Payment", blank= True, null= True)
    receipt = models.IntegerField(default = 0, verbose_name = "Receipt", blank= True, null= True)
    admin_approved = models.BooleanField(default= False)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('driver-update', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):

        self.bata -= (self.advance - self.expense)

        if self.is_settled == True:
            self.bata = 0
            self.is_settled = False
        super(Driver, self).save(*args, **kwargs)  

    class Meta:
        # managed = True
        db_table = 'Driver'    

class Tripsheet(models.Model):

    veh = models.ForeignKey(Vehiclemaster, verbose_name = 'Vehicle number', on_delete = models.DO_NOTHING)
    driver = models.ForeignKey(Driver, verbose_name = "Assigned Driver", on_delete = models.DO_NOTHING)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'Tripsheet'

class EntryTable(models.Model):

    # veh = models.CharField(max_length= 30, verbose_name= 'Vehicle number', validators=[
    #         RegexValidator(
    #             regex='^[A-Z]{2}[ -][0-9]{1,2}(?: [A-Z])?(?: [A-Z]*)? [0-9]{4}$',
    #             message='Enter a valid vehicle number',
    #         ),
    #     ])
    veh = models.CharField(max_length= 30, verbose_name= 'Vehicle number',)
    purpose = models.CharField(max_length= 30, verbose_name= 'Purpose')
    in_time = models.DateTimeField(verbose_name= 'In Time', blank= True, null= True)
    out_time = models.DateTimeField(verbose_name= 'Out Time', blank= True, null= True)


    def __str__(self):
        return str(self.veh)



class FuelLog(models.Model):
    veh = models.ForeignKey(Vehiclemaster, verbose_name = 'Vehicle number', on_delete = models.DO_NOTHING)
    size = models.CharField(max_length = 15, verbose_name= 'Vehicle size')
    manfr = models.CharField(max_length = 25, verbose_name= 'Manufacturer')
    no = models.CharField(max_length = 20, verbose_name='Indent no', unique = True)   #CharField 
    date = models.DateField(default = datetime.now, verbose_name = 'Date')
    diesel = models.IntegerField(verbose_name = 'Diesel in Litres')
    petrol = models.IntegerField(verbose_name = 'Petrol in Litres', blank = True, null = True)
    lub = models.IntegerField(verbose_name = 'Lube oil in Litres', blank = True, null = True)
    othr = models.IntegerField(verbose_name = 'Others', blank = True, null = True,)
    odo = models.IntegerField(verbose_name = 'Odo reading(in km)')
    fuel = models.IntegerField(verbose_name = 'Fuel filled(in Rs)')

    def clean(self):
        if self.veh:
            self.size = self.veh.size
            self.manfr = self.veh.manfr

    class Meta:
        db_table = 'Fuellog'

    def __str__(self):
        return str(self.no)

class Trip(models.Model):

    ACE = 1.00
    Dosth = 1.70
    TEN = 2.00
    FORTEEN = 2.30
    SEVENTEEN = 2.60
    NINETEEN = 2.90
    TWENTY = 3.10
    TWENTYTWO = 3.10

    VEH_CHOICES = (
=======
	# code = models.CharField(max_length = 10, verbose_name = "Driver ID")
	name = models.CharField(max_length = 30, verbose_name = 'Driver name', unique = True)
	phone = models.CharField(max_length = 12, verbose_name = 'Phone number')
	# region = models.ForeignKey(Region, on_delete = models.CASCADE, verbose_name = 'Region')
	bata = models.IntegerField(null = True, blank = True, default = 0, verbose_name = "BATA")
	advance = models.IntegerField(default = 0, verbose_name = "Advance")
	expense = models.IntegerField(default = 0, verbose_name = "Expense")
	is_settled = models.BooleanField(default = False, verbose_name = "Salary settlement")
	# activity = models.TextField(blank = True, null = True, verbose_name = "Activity")
	# address = models.TextField(blank = True, null = True, verbose_name = "Address")
	# salary = models.IntegerField(default = 0, verbose_name = "Fixed salary")
	photo = models.ImageField(upload_to = 'media', null = True, blank = True)
	# license = models.FileField(upload_to = 'media', null = True, blank = True)
	# rationcard = models.FileField(upload_to = 'media', null = True, blank = True)
	# aadhar = models.FileField(upload_to = 'media', null = True, blank = True)
	# is_temp = models.BooleanField(default = False, verbose_name = "Permanent")

	def __str__(self):
		return str(self.name)

	def get_absolute_url(self):
		return reverse('driver-update', kwargs={'pk': self.pk})

	def save(self, *args, **kwargs):

		self.bata -= (self.advance - self.expense)

		if self.is_settled == True:
			self.bata = 0
			self.is_settled = False
		super(Driver, self).save(*args, **kwargs)  

	class Meta:
		# managed = True
		db_table = 'Driver'	

class Tripsheet(models.Model):

	veh = models.ForeignKey(Vehiclemaster, verbose_name = 'Vehicle number', on_delete = models.DO_NOTHING)
	driver = models.ForeignKey(Driver, verbose_name = "Assigned Driver", on_delete = models.DO_NOTHING)

	def __str__(self):
		return str(self.id)


class FuelLog(models.Model):
	veh = models.ForeignKey(Vehiclemaster, verbose_name = 'Vehicle number', on_delete = models.DO_NOTHING)
	size = models.CharField(max_length = 15, verbose_name= 'Vehicle size')
	manfr = models.CharField(max_length = 25, verbose_name= 'Manufacturer')
	no = models.CharField(max_length = 20, verbose_name='Indent no', unique = True)   #CharField 
	date = models.DateField(default = datetime.now, verbose_name = 'Date')
	diesel = models.IntegerField(verbose_name = 'Diesel in Litres')
	petrol = models.IntegerField(verbose_name = 'Petrol in Litres', blank = True, null = True)
	lub = models.IntegerField(verbose_name = 'Lube oil in Litres', blank = True, null = True)
	othr = models.IntegerField(verbose_name = 'Others', blank = True, null = True,)
	odo = models.IntegerField(verbose_name = 'Odo reading(in km)')
	fuel = models.IntegerField(verbose_name = 'Fuel filled(in Rs)')

	def clean(self):
		if self.veh:
			self.size = self.veh.size
			self.manfr = self.veh.manfr

	class Meta:
		managed = True

	def __str__(self):
		return str(self.no)

class Trip(models.Model):

	ACE = 1.00
	Dosth = 1.70
	TEN = 2.00
	FORTEEN = 2.30
	SEVENTEEN = 2.60
	NINETEEN = 2.90
	TWENTY = 3.10
	TWENTYTWO = 3.10

	VEH_CHOICES = (
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b
        (ACE, 'ACE'),
        (Dosth, 'Dosth'),
        (TEN, '10.5FT'),
        (FORTEEN, '14FT'),
        (SEVENTEEN, '17FT'),
        (NINETEEN, '19FT'),
        (TWENTY, '20FT'),
<<<<<<< HEAD
        (TWENTYTWO, '22FT'),
    )
    tripno = models.CharField(max_length = 20, verbose_name = "Trip Number")
    no = models.CharField(max_length = 20, verbose_name = "Number")
    driver = models.ForeignKey(Driver, on_delete = models.DO_NOTHING, blank = True, null = True, verbose_name = "Driver")
    veh = models.ForeignKey(Vehiclemaster, verbose_name = "Vehicle used", on_delete = models.DO_NOTHING)
    ftype = models.FloatField(null = True, blank = True, verbose_name = "Vehicle Type", choices = VEH_CHOICES)
    advance = models.IntegerField(null = True, blank = True, verbose_name = "Advance")
    start = models.IntegerField( verbose_name="Starting odo")
    end = models.IntegerField(verbose_name = "Ending odo")
    km = models.IntegerField(verbose_name = "Distance(in kms)")
    source = models.CharField(max_length = 60, verbose_name = "From")
    dest = models.CharField(max_length = 60, verbose_name = "To")
    region = models.ForeignKey(Region, on_delete = models.DO_NOTHING, null = True, blank = True, verbose_name = "Region")
    lr = models.CharField(max_length = 100, verbose_name = "LR Number")
    date = models.DateField(default = datetime.now, verbose_name = "Date")
    is_approved = models.BooleanField(default = False, verbose_name = "Approve Trip")
    bata = models.IntegerField(default = 0, verbose_name = "BATA")
    status = models.BooleanField(default= 0, verbose_name= 'Open')
    # billno=models.CharField(max_length = 20,verbose_name='LrTran_waybillno')            #neww
    # km=models.CharField(max_length = 20,verbose_name='LrTran_Km')
    # kmrate=models.CharField(max_length = 20,verbose_name='LrTran_Kmrate')
    # driver=models.CharField(max_length = 20,verbose_name='LrTran_DriverDtls')
    # frtbillno=models.CharField(max_length = 20,verbose_name='LrTran_Frtypebillno')    
    # salary = models.IntegerField(default = 0, verbose_name = "Salary")
    
    class Meta:
        db_table = 'Trip'
        unique_together = ('no', 'driver',)

    def __str__(self):
        return str(self.no)

    def get_absolute_url(self):
        return reverse('trip-update', kwargs={'pk': self.pk})


    def save(self, *args, **kwargs):
        self.km = self.end - self.start
        if self.is_approved == True:
            self.km = self.end - self.start
            self.bata = self.ftype * self.km
        super(Trip, self).save(*args, **kwargs)       

@receiver(post_save, sender=Trip)
def _post_save_receiver(sender, instance, **kwargs):
    new_instance = Driver.objects.get(id = instance.driver_id)

    Driver.objects.filter(id = instance.driver_id).update(bata=F('bata') + instance.bata)

=======
		(TWENTYTWO, '22FT'),
	)
	no = models.CharField(max_length = 20, verbose_name = "Number")
	driver = models.ForeignKey(Driver, on_delete = models.DO_NOTHING, blank = True, null = True, verbose_name = "Driver")
	veh = models.ForeignKey(Vehiclemaster, verbose_name = "Vehicle used", on_delete = models.DO_NOTHING)
	ftype = models.FloatField(null = True, blank = True, verbose_name = "Vehicle Type", choices = VEH_CHOICES)
	advance = models.IntegerField(null = True, blank = True, verbose_name = "Advance")
	start = models.IntegerField( verbose_name="Starting odo")
	end = models.IntegerField(verbose_name = "Ending odo")
	km = models.IntegerField(verbose_name = "Distance(in kms)")
	source = models.CharField(max_length = 60, verbose_name = "From")
	dest = models.CharField(max_length = 60, verbose_name = "To")
	# region = models.ForeignKey(Region, on_delete = models.DO_NOTHING, null = True, blank = True, verbose_name = "Region")
	lr = models.CharField(max_length = 100, verbose_name = "LR Number")
	date = models.DateField(default = datetime.now, verbose_name = "Date")
	is_approved = models.BooleanField(default = False, verbose_name = "Approve Trip")
	bata = models.IntegerField(default = 0, verbose_name = "BATA")
	# billno=models.CharField(max_length = 20,verbose_name='LrTran_waybillno')			#neww
	# km=models.CharField(max_length = 20,verbose_name='LrTran_Km')
	# kmrate=models.CharField(max_length = 20,verbose_name='LrTran_Kmrate')
	# driver=models.CharField(max_length = 20,verbose_name='LrTran_DriverDtls')
	# frtbillno=models.CharField(max_length = 20,verbose_name='LrTran_Frtypebillno')	
	# salary = models.IntegerField(default = 0, verbose_name = "Salary")
	
	class Meta:

		unique_together = ('no', 'driver',)

	def __str__(self):
		return str(self.no)

	def get_absolute_url(self):
		return reverse('trip-update', kwargs={'pk': self.pk})


	def save(self, *args, **kwargs):
		self.km = self.end - self.start
		if self.is_approved == True:
			self.km = self.end - self.start
			self.bata = self.ftype * self.km
		super(Trip, self).save(*args, **kwargs)       

@receiver(post_save, sender=Trip)
def _post_save_receiver(sender, instance, **kwargs):
	new_instance = Driver.objects.get(id = instance.driver_id)

	Driver.objects.filter(id = instance.driver_id).update(bata=F('bata') + instance.bata)



# class Userdetails(AbstractUser): 
#     # usrd_id = models.AutoField(primary_key = True)
#     usrd_usrcatpntr = models.ForeignKey(Usercategory,null = True, blank = True, verbose_name= 'User Type', on_delete = models.CASCADE)
#     usrd_code = models.IntegerField(blank=True, null=True)
#     usrd_assinedwhm = models.ForeignKey(Companywarehousemaster, verbose_name= 'Assigned Warehouse', null = True, blank = True, on_delete = models.CASCADE)
#     usrd_name = models.CharField(max_length=50, verbose_name='Employee name', unique=True, blank=True, null=True)
#     password = models.CharField(max_length=256, blank=True, null=True)
#     usrd_slno = models.IntegerField(blank=True, null=True)
#     usrd_remarks = models.CharField(max_length=250, blank=True, null=True)
#     usrd_active = models.CharField(max_length=1, verbose_name='User Status', blank=True, null=True)
#     usrd_makerid = models.IntegerField(blank=True, null=True)
#     usrd_maketime = models.DateTimeField(blank=True, null=True)
#     usrd_logcount = models.IntegerField(blank=True, null=True)
#     usrd_logattempt = models.IntegerField(blank=True, null=True)
#     usrd_region = models.ForeignKey(Region, on_delete = models.CASCADE, null = True, blank = True, verbose_name = "Region")
    
#     # USERNAME_FIELD = 'usrd_name'
#     # class Meta:
#     #     db_table = 'userdetails'

#     def __str__(self):
#         return str(self.usrd_name)
>>>>>>> 32ca857026708f222b9c07f2a31fd338ffc1149b
