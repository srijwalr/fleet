# from django.db import models

# # Create your models here.

# class Vehiclecategory(models.Model):
#     vehcat_id = models.IntegerField(primary_key = True, default = 1)
#     vehcat_code = models.CharField(max_length=50,verbose_name='Code', blank=True, null=True)
#     vehcat_desc = models.CharField(max_length=100,verbose_name='Description', blank=True, null=True)
#     vehcat_wtcapacity = models.FloatField(verbose_name='Weight capacity', blank=True, null=True)
#     vehcat_length = models.FloatField(verbose_name='Length', blank=True, null=True)
#     vehcat_width = models.FloatField(verbose_name='Width', blank=True, null=True)
#     vehcat_ft = models.CharField(max_length=50, blank=True, null=True)
#     vehcat_kmrate = models.DecimalField(max_digits=18, verbose_name='KM Rate', decimal_places=2, blank=True, null=True)
#     vehcat_slno = models.IntegerField(verbose_name='Serial no.', blank=True, null=True)
#     vehcat_active = models.CharField(max_length=1, blank=True, null=True)
#     vehcat_remarks = models.CharField(max_length=250,verbose_name='Remarks', blank=True, null=True)
#     vehcat_makerid = models.IntegerField(blank=True, null=True)
#     vehcat_maketime = models.DateTimeField(blank=True, null=True)

#     def __str__(self):
#         return self.vehcat_code
#     class Meta:
#         db_table = 'VehicleCategory'
  
# class Freighttypes(models.Model):
#     fretype_id = models.IntegerField(primary_key = True,default = 1)
#     fretype_code = models.CharField(max_length=50,verbose_name='Code', blank=True, null=True)
#     fretype_desc = models.CharField(max_length=100,verbose_name='Description', blank=True, null=True)
#     fretype_slno = models.IntegerField(verbose_name='Serial no.', blank=True, null=True)
#     fretype_remarks = models.CharField(max_length=250,verbose_name='Remarks', blank=True, null=True)
#     fretype_active = models.CharField(max_length=1,verbose_name='Status', blank=True, null=True)
#     fretype_nnc_code = models.CharField(max_length=10, blank=True, null=True)
#     fretype_whmcode = models.IntegerField(blank=True, null=True)
    
#     def __str__(self):
#         return self.fretype_desc
#     class Meta:
#         db_table = 'Freighttypes'
 

# class Vehiclemaster(models.Model):
#     vehmas_id = models.IntegerField(primary_key = True, default = 1)
#     vehmas_code = models.CharField(max_length=50,verbose_name='Vehicle Number', blank=True, null=True)
#     vehmas_desc = models.CharField(max_length=100,verbose_name='Description', blank=True, null=True)
#     vehmas_catpntr = models.ForeignKey(Vehiclecategory, db_column = 'vehcat_id',verbose_name='Category',  on_delete = models.CASCADE)
#     vehmas_drivername = models.CharField(max_length= 20, verbose_name= 'Driver Name', blank=True, null = True)
#     vehmas_phone = models.CharField(max_length= 15,verbose_name='Phone Number', blank=True, null=True )
#     vehmas_frtyppntr = models.ForeignKey(Freighttypes,db_column = 'fretype_id', verbose_name='Vehicle Mode', blank=True, null=True, on_delete = models.CASCADE)
#     vehmas_modepntr = models.IntegerField(blank=True, null=True)
#     vehmas_slno = models.IntegerField(blank=True, null=True)
#     vehmas_active = models.CharField(max_length=1,verbose_name='Status', blank=True, null=True)
#     vehmas_remarks = models.CharField(max_length=250, blank=True, null=True)
#     vehmas_makerid = models.IntegerField(blank=True, null=True)
#     vehmas_maketime = models.DateTimeField(blank=True, null=True)
#     vehmas_clntpntr = models.IntegerField(blank=True, null=True)

#     def __str__(self):
#         return str(self.vehmas_desc)
#     class Meta:
#         db_table = 'VehicleMaster'


# class Tyre(models.Model):

#     DESC_CHOICES = (
#         ('FL', 'Front Left'),
#         ('FR', 'Front Right'),
#         ('BL', 'Back Left'),
#         ('BR', 'Back Right'),
#         ('BL1', 'Back Left+1'),
#         ('BR1', 'Back Right+1'),
#         ('ST', 'Stepney'),
#         ('OT', 'Others'),
#     )

#     flt = models.ForeignKey(Vehiclemaster, on_delete = models.CASCADE)
#     desc = models.CharField(max_length = 7, verbose_name = 'Description', choices = DESC_CHOICES)
#     dtl = models.CharField(max_length = 15, verbose_name = 'Tyre no.')
#     make = models.CharField(max_length = 25,verbose_name = 'Make')

#     class Meta:
#         managed = True

#     def __str__(self):
#         return str(self.dtl)
#     