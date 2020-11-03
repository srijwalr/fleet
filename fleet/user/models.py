# from django.db import models
# from app.models import Region
# from django.contrib.auth.models import AbstractUser
# # Create your models here.

# class Usercategory(models.Model):
#     usrcat_id = models.IntegerField(primary_key = True, default = 1)
#     usrcat_code = models.CharField(max_length=4, blank=True, null=True)
#     usercat_desc = models.CharField(max_length=20, blank=True, null=True)
#     usercat_remarks = models.CharField(max_length=250, blank=True, null=True)
#     usercat_active = models.CharField(max_length=1, blank=True, null=True)
#     usercat_slno = models.IntegerField(blank=True, null=True)


#     class Meta:
#         db_table = 'UserCategory'

#     def __str__(self):
#         return str(self.usercat_desc)

# class Profile(AbstractUser): 
#     # usrd_id = models.AutoField(primary_key = True)
#     usrcatpntr = models.ForeignKey(Usercategory,null = True, blank = True, verbose_name= 'User Type', on_delete = models.CASCADE)
#     code = models.IntegerField(blank=True, null=True)
#     name = models.CharField(max_length=50, verbose_name='Employee name', unique=True, blank=True, null=True)
#     password = models.CharField(max_length=256, blank=True, null=True)
#     slno = models.IntegerField(blank=True, null=True)
#     remarks = models.CharField(max_length=250, blank=True, null=True)
#     active = models.CharField(max_length=1, verbose_name='User Status', blank=True, null=True)
#     makerid = models.IntegerField(blank=True, null=True)
#     maketime = models.DateTimeField(blank=True, null=True)
#     logcount = models.IntegerField(blank=True, null=True)
#     logattempt = models.IntegerField(blank=True, null=True)
#     region = models.ForeignKey(Region, on_delete = models.CASCADE, null = True, blank = True, verbose_name = "Region")
    
#     # USERNAME_FIELD = 'name'
#     # class Meta:
#     #     db_table = 'userdetails'

#     def __str__(self):
#         return str(self.username)
