# from django.db import models

# # Create your models here.


# class Cosingnormaster(models.Model):
#     # consgnrm_id = models.AutoField(primary_key=True)
#     consgnrm_code = models.CharField(max_length=50, blank=True, null=True)
#     consgnrm_clntmaspntr = models.IntegerField(blank=True, null=True)
#     consgnrm_whmcode = models.IntegerField(blank=True, null=True)
#     consgnrm_name = models.CharField(max_length=100, blank=True, null=True)
#     consgnrm_address = models.CharField(max_length=400, blank=True, null=True)
#     cosngnrm_desc = models.CharField(max_length=250, blank=True, null=True)
#     cosngnrm_slno = models.IntegerField(blank=True, null=True)
#     consgnrm_remarks = models.CharField(max_length=250, blank=True, null=True)
#     consgnrm_active = models.CharField(max_length=1, blank=True, null=True)
#     consgnrm_makerid = models.IntegerField(blank=True, null=True)
#     consgnrm_maketime = models.DateTimeField(blank=True, null=True)

#     # class Meta:
#     #     managed = False
#     #     db_table = 'cosingnormaster'    

# class Companyzonemaster(models.Model):
#     # com_zmasid = models.AutoField(primary_key=True)
#     com_zmasdesc = models.CharField(max_length=50, blank=True, null=True)
#     com_zmasname = models.CharField(max_length=50, blank=True, null=True)
#     com_zmascommaspntr = models.IntegerField(blank=True, null=True)
#     com_zmasslno = models.IntegerField(blank=True, null=True)
#     com_zmasremarks = models.CharField(max_length=250, blank=True, null=True)
#     com_zmasactive = models.CharField(max_length=2, blank=True, null=True)

#     # class Meta:
#     #     managed = False
#     #     db_table = 'companyzonemaster'


# class Companymaster(models.Model):
#     # com_masid = models.AutoField(primary_key=True)
#     com_masdesc = models.CharField(max_length=50, blank=True, null=True)
#     com_masname = models.CharField(max_length=150, blank=True, null=True)
#     com_masaddress = models.CharField(max_length=250, blank=True, null=True)
#     com_phone = models.CharField(max_length=12, blank=True, null=True)
#     com_slno = models.IntegerField(blank=True, null=True)
#     com_remarks = models.CharField(max_length=250, blank=True, null=True)
#     com_active = models.CharField(max_length=2, blank=True, null=True)

#     # class Meta:
#     #     managed = False
#     #     db_table = 'companymaster'

# class Couriermaster(models.Model):
#     # courmas_id = models.AutoField(primary_key=True)
#     courmas_code = models.CharField(max_length=50, blank=True, null=True)
#     courmas_desc = models.CharField(max_length=100, blank=True, null=True)
#     courmas_slno = models.IntegerField(blank=True, null=True)
#     courmas_active = models.CharField(max_length=1, blank=True, null=True)
#     courmas_remarks = models.CharField(max_length=250, blank=True, null=True)
#     courmas_makerid = models.IntegerField(blank=True, null=True)
#     courmas_maketime = models.DateTimeField(blank=True, null=True)
#     courmas_clntcode = models.IntegerField(blank=True, null=True)

#     # class Meta:
#     #     managed = False
#     #     db_table = 'couriermaster'

# class Productcategory(models.Model):
#     # procat_id = models.IntegerField( blank=True, null=True)
#     procat_code = models.CharField(max_length=25, verbose_name='Code', blank=True, null=True)
#     procat_desc = models.CharField(max_length=100, verbose_name='Description', blank=True, null=True)
#     procat_slno = models.IntegerField( verbose_name='Serial no.', blank=True, null=True)
#     procat_active = models.CharField( verbose_name='Status', max_length=1, blank=True, null=True)
#     procat_remarks = models.CharField(max_length=250,  verbose_name='Remarks', blank=True, null=True)
#     procat_makerid = models.IntegerField(blank=True, null=True)
#     procat_maketime = models.DateTimeField(blank=True, null=True)
#     procat_clntpntr = models.IntegerField(blank=True, null=True)
    
#     def __str__(self):
#         return self.procat_desc
#     # class Meta:
#     #     db_table = 'productcategory'


# class Employeedesignationmaster(models.Model):
#     # empdesig_id = models.AutoField(primary_key=True)
#     empdesig_code = models.CharField(max_length=50, blank=True, null=True)
#     empdesig_name = models.CharField(max_length=150, blank=True, null=True)
#     empdesig_slno = models.IntegerField(blank=True, null=True)
#     empdesig_remarks = models.CharField(max_length=250, blank=True, null=True)
#     empdesig_active = models.CharField(max_length=1, blank=True, null=True)
#     empdesig_makingtime = models.DateTimeField(blank=True, null=True)
#     empdesig_makerid = models.IntegerField(blank=True, null=True)

#     # class Meta:
#     #     managed = False
#     #     db_table = 'employeedesignationmaster'

# class Employeetypemaster(models.Model):
#     # emptyp_id = models.AutoField(primary_key=True)
#     emptyp_code = models.CharField(max_length=50, blank=True, null=True)
#     emptyp_desc = models.CharField(max_length=50, blank=True, null=True)
#     emptyp_active = models.CharField(max_length=1, blank=True, null=True)
#     emptyp_slno = models.IntegerField(blank=True, null=True)
#     emptyp_remarks = models.CharField(max_length=250, blank=True, null=True)
#     emptyp_makingtime = models.DateTimeField(blank=True, null=True)
#     emptyp_makerid = models.IntegerField(blank=True, null=True)

#     # class Meta:
#     #     managed = False
#     #     db_table = 'employeetypemaster'

# class Employeemaster(models.Model):
#     # empmas_id = models.AutoField(primary_key=True)
#     empmas_code = models.CharField(max_length=50, blank=True, null=True)
#     empmas_empdesigpntr = models.IntegerField(blank=True, null=True)
#     empmas_emptyppntr = models.IntegerField(blank=True, null=True)
#     empmas_empwhmcode = models.IntegerField(blank=True, null=True)
#     empmas_name = models.CharField(max_length=150, blank=True, null=True)
#     empmas_address = models.TextField(blank=True, null=True)
#     empmas_phone = models.CharField(max_length=10, blank=True, null=True)
#     empmas_effectfrom = models.DateTimeField(blank=True, null=True)
#     empmas_retireddate = models.DateTimeField(blank=True, null=True)
#     empmas_slno = models.IntegerField(blank=True, null=True)
#     empmas_active = models.CharField(max_length=1, blank=True, null=True)
#     empmas_remarks = models.CharField(max_length=250, blank=True, null=True)

#     # class Meta:
#     #     managed = False
#     #     db_table = 'employeemaster'


# class Firmmaster(models.Model):
#     # frmm_id = models.BigAutoField(primary_key=True)
#     frmm_code = models.CharField(max_length=20, blank=True, null=True)
#     frmm_name = models.CharField(max_length=25, blank=True, null=True)
#     frmm_adress = models.CharField(max_length=250, blank=True, null=True)
#     frmm_contact = models.CharField(max_length=20, blank=True, null=True)
#     frmm_slno = models.IntegerField(blank=True, null=True)
#     frmm_active = models.CharField(max_length=1, blank=True, null=True)
#     frmm_remarks = models.CharField(max_length=250, blank=True, null=True)

#     # class Meta:
#     #     managed = False
#     #     db_table = 'firmmaster'


# class Productsubcategory(models.Model):
#     # proscat_id = models.IntegerField(blank=True, null=True )
#     proscat_procatpntr = models.ForeignKey(Productcategory, verbose_name='Category',  on_delete = models.CASCADE)
#     proscat_code = models.CharField(max_length=50, verbose_name='Code',  blank=True, null=True)
#     proscat_desc = models.CharField(max_length=100, verbose_name='Description',blank=True, null=True)
#     proscat_volume = models.FloatField(blank=True,verbose_name='Volume', null=True)
#     proscat_weight = models.FloatField(blank=True,verbose_name='Weight', null=True)
#     proscat_width = models.FloatField(blank=True,verbose_name='Width', null=True)
#     proscat_length = models.FloatField(blank=True,verbose_name='Length', null=True)
#     proscat_slno = models.IntegerField(verbose_name='Serial no.',blank=True, null=True)
#     proscat_active = models.CharField(max_length=1,verbose_name='Status', blank=True, null=True)
#     proscat_remarks = models.CharField(max_length=250,verbose_name='Remarks', blank=True, null=True)
#     proscat_makerid = models.IntegerField(blank=True, null=True)
#     proscat_maketime = models.DateTimeField(blank=True, null=True)
#     proscat_clntcode = models.IntegerField(blank=True, null=True)


#     # class Meta:
#     #     db_table = 'productsubcategory'

# class Groupcode(models.Model):
#     material_code = models.CharField(max_length=255, blank=True, null=True)
#     material = models.CharField(max_length=255, blank=True, null=True)
#     group_code = models.CharField(max_length=255, blank=True, null=True)
#     group = models.CharField(max_length=255, blank=True, null=True)
#     div_no = models.CharField(max_length=255, blank=True, null=True)
#     division = models.CharField(max_length=255, blank=True, null=True)

#     # class Meta:
#     #     managed = False
#     #     db_table = 'groupcode_'

# class Productgroup(models.Model):
#     # prog_id = models.AutoField(primary_key=True)
#     prog_code = models.CharField(max_length=50, blank=True, null=True)
#     prog_desc = models.CharField(max_length=150, blank=True, null=True)
#     prog_slno = models.IntegerField(blank=True, null=True)
#     prog_rmrks = models.TextField(blank=True, null=True)
#     prog_status = models.CharField(max_length=1, blank=True, null=True)
#     prog_clntpntr = models.IntegerField(blank=True, null=True)
    
#     # class Meta:
#     #     db_table = 'productgroup'

# class Productmaster(models.Model):
#     # promas_id = models.IntegerField( blank=True, null=True)
#     promas_code = models.CharField(max_length=50, verbose_name= 'Code', blank=True, null=True)
#     promas_desc = models.CharField(max_length=300, verbose_name= 'Description', blank=True, null=True)
#     promas_quantity = models.IntegerField( verbose_name= 'Quantity',blank=True, null=True)
#     promas_procat_pntr = models.ForeignKey(Productcategory,blank=True, null=True,  verbose_name= 'Category',  on_delete = models.CASCADE)
#     promas_proscat_pntr = models.ForeignKey(Productsubcategory,blank=True, null=True,  verbose_name= 'Sub category',  on_delete = models.CASCADE)
#     promas_group_pntr = models.ForeignKey(Productgroup,blank=True, null=True,  on_delete = models.CASCADE)
#     promas_slno = models.IntegerField(blank=True, verbose_name= 'Serial no.', null=True)
#     promas_active = models.CharField(max_length=1, verbose_name= 'Status', blank=True, null=True)
#     promas_remarks = models.CharField(max_length=250, verbose_name= 'Remarks', blank=True, null=True)
#     promas_makerid = models.IntegerField(blank=True, null=True)
#     promas_maketime = models.DateTimeField(blank=True, null=True)
#     promas_clntcode = models.IntegerField(blank=True, null=True)

#     # class Meta:
#     #     db_table = 'productmaster'        

# class Vehiclecategory(models.Model):
#     # vehcat_id = models.IntegerField( blank=True, null=True)
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
#     # class Meta:
#     #     db_table = 'vehiclecategory'


# class Freighttypes(models.Model):
#     # fretype_id = models.IntegerField( blank=True, null=True)
#     fretype_code = models.CharField(max_length=50,verbose_name='Code', blank=True, null=True)
#     fretype_desc = models.CharField(max_length=100,verbose_name='Description', blank=True, null=True)
#     fretype_slno = models.IntegerField(verbose_name='Serial no.', blank=True, null=True)
#     fretype_remarks = models.CharField(max_length=250,verbose_name='Remarks', blank=True, null=True)
#     fretype_active = models.CharField(max_length=1,verbose_name='Status', blank=True, null=True)
#     fretype_nnc_code = models.CharField(max_length=10, blank=True, null=True)
#     fretype_whmcode = models.IntegerField(blank=True, null=True)
    
#     def __str__(self):
#         return self.fretype_desc
#     # class Meta:
#     #     db_table = 'freighttypes'
 
     
# class Vehiclemaster(models.Model):
#     # vehmas_id = models.IntegerField( blank=True, null=True)
#     vehmas_code = models.CharField(max_length=50,verbose_name='Vehicle Number', blank=True, null=True)
#     vehmas_desc = models.CharField(max_length=100,verbose_name='Description', blank=True, null=True)
#     vehmas_catpntr = models.ForeignKey(Vehiclecategory,verbose_name='Category',  on_delete = models.CASCADE)
#     vehmas_drivername = models.CharField(max_length= 20, verbose_name= 'Driver Name', blank=True, null = True)
#     vehmas_phone = models.CharField(max_length= 15,verbose_name='Phone Number', blank=True, null=True )
#     vehmas_frtyppntr = models.ForeignKey(Freighttypes, verbose_name='Vehicle Mode', blank=True, null=True, on_delete = models.CASCADE)
#     vehmas_modepntr = models.IntegerField(blank=True, null=True)
#     vehmas_slno = models.IntegerField(blank=True, null=True)
#     vehmas_active = models.CharField(max_length=1,verbose_name='Status', blank=True, null=True)
#     vehmas_remarks = models.CharField(max_length=250, blank=True, null=True)
#     vehmas_makerid = models.IntegerField(blank=True, null=True)
#     vehmas_maketime = models.DateTimeField(blank=True, null=True)
#     vehmas_clntpntr = models.IntegerField(blank=True, null=True)

#     def __str__(self):
#         return str(self.vehmas_desc)
#     # class Meta:
#     #     db_table = 'vehiclemaster'


# class Routemaster(models.Model):
#     # rtm_id = models.IntegerField( blank=True, null=True)
#     rtm_code = models.CharField(max_length=50,verbose_name='Code', blank=True, null=True)
#     rtm_desc = models.CharField(max_length=100, verbose_name='Description')
#     rtm_dist = models.CharField(max_length=50, verbose_name='Distance')
#     rtm_slno = models.IntegerField(verbose_name='Serial no.', blank=True, null=True)
#     rtm_remarks = models.CharField(max_length=250,verbose_name='Remarks', blank=True, null=True)
#     rtm_active = models.CharField(max_length=1,verbose_name='Status', blank=True, null=True)
#     rtm_details = models.CharField(max_length=250,verbose_name='Details', blank=True, null=True)

#     # class Meta:
#     #     db_table = 'routemaster'



# class Freightmodes(models.Model):
#     # fremodes_id = models.AutoField(primary_key=True)
#     fremodes_code = models.CharField(max_length=50, blank=True, null=True)
#     fremodes_desc = models.CharField(max_length=100, blank=True, null=True)
#     fremodes_slno = models.IntegerField(blank=True, null=True)
#     fremodes_remarks = models.CharField(max_length=250, blank=True, null=True)
#     fremodes_active = models.CharField(max_length=1, blank=True, null=True)

#     # class Meta:
#     #     managed = False
#     #     db_table = 'freightmodes'


# class Freightforroute(models.Model):
#     # fght_id = models.BigIntegerField( blank=True, null=True)
#     fght_fretypeptr = models.IntegerField(verbose_name='Code', blank=True, null=True)
#     fght_routeptr = models.IntegerField(verbose_name='Route type', blank=True, null=True)
#     fght_basefreight = models.IntegerField(verbose_name='Base Freight', blank=True, null=True)
#     fght_kmrate = models.DecimalField(max_digits=18, decimal_places=2,verbose_name='KM Rate', blank=True, null=True)
#     fght_vehcatptr = models.IntegerField(verbose_name='Vehicle Category', blank=True, null=True)
#     fght_slno = models.IntegerField(verbose_name='Serial no.', blank=True, null=True)
#     fght_remarks = models.CharField(max_length=250,verbose_name='Remarks', blank=True, null=True)
#     fght_active = models.CharField(max_length=1,verbose_name='Status', blank=True, null=True)

#     # class Meta:
#     #     db_table = 'freightforroute'

# class Cosingneemaster(models.Model):    
#     # consgnemid = models.IntegerField( blank=True, null=True)
#     consgnem_code = models.CharField(max_length=50, verbose_name= 'Consignee code', blank=True, null=True, unique= True)
#     consgnem_name = models.CharField(max_length=100, verbose_name= 'Consignee name',  blank=True, null=True)
#     consgnem_branch = models.CharField(max_length=50, verbose_name= 'Consignee branch', blank=True, null=True)
#     consgnem_address = models.CharField(max_length=500, verbose_name= 'Consignee address',  blank=True, null=True)
#     consgnem_city = models.CharField(max_length=50, verbose_name= 'Consignee city',  blank=True, null=True)
#     consgnem_district = models.CharField(max_length=50, verbose_name= 'Consignee district',  blank=True, null=True)
#     consgnem_pincode = models.IntegerField(blank=True,verbose_name= 'Consignee pincode',  null=True)
#     consgnem_routtyp = models.CharField(max_length=20,verbose_name= 'Consignee route type',  blank=True, null=True)
#     consgnem_gsttin = models.CharField(max_length=25,verbose_name= 'Consignee GST',  blank=True, null=True)
#     consgnem_pan = models.CharField(max_length=25,verbose_name= 'Consignee PAN',  blank=True, null=True)
#     consgnem_distance = models.FloatField(blank=True, null=True, verbose_name= 'Consignee distance')
#     cosngnrm_slno = models.IntegerField(blank=True,  null=True)
#     consgnem_remarks = models.CharField(max_length=250,  blank=True, null=True)
#     consgnem_active = models.CharField(max_length=1,  blank=True, null=True)
#     consgnem_makerid = models.IntegerField( blank=True, null=True)
#     consgnem_maketime = models.DateTimeField( blank=True, null=True)
#     consgnem_routepntr = models.IntegerField(verbose_name='Consignee Route', blank=True, null=True)
#     consgnem_clntpntr = models.IntegerField( blank=True, null=True)

#     def __str__(self):
#         return self.consgnem_code

# class Meta:
# db_table = 'cosingneemaster' 
