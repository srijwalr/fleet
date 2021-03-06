# Generated by Django 2.1.15 on 2020-12-01 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201201_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='region',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.Region', verbose_name='Region'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='region',
            field=models.ForeignKey(blank=True, db_column='region_id', default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Region', verbose_name='Region'),
        ),
        migrations.AddField(
            model_name='profile',
            name='usrcatpntr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Usercat', verbose_name='User Type'),
        ),
        migrations.AddField(
            model_name='trip',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.Region', verbose_name='Region'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='acc',
            field=models.ManyToManyField(blank=True, to='app.Accessories', verbose_name='Accessories'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='activity',
            field=models.TextField(blank=True, null=True, verbose_name='Activity'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='btrymodel',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Battery Model'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='btryno',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Battery code'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='chno',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Chassis number'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='engno',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Engine number'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='fitndate',
            field=models.DateField(blank=True, null=True, verbose_name='Fitness Expiry'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='fitnfile',
            field=models.FileField(blank=True, default='', null=True, upload_to='media', verbose_name='Fitness File'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='fitnno',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Fitness number'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='fstatus',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='ftype',
            field=models.CharField(choices=[('D', 'Diesel'), ('P', 'Petrol'), ('E', 'Electric')], default='D', max_length=10, verbose_name='Fuel type'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='insamt',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Insurance amount'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='insdate',
            field=models.DateField(blank=True, null=True, verbose_name='Insurance expiry'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='insfile',
            field=models.FileField(blank=True, default='', null=True, upload_to='media', verbose_name='Insurance File'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='insno',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Insurance Policy number'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='istatus',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='manfr',
            field=models.CharField(default='Test', max_length=25, verbose_name='Manufacturer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='model',
            field=models.CharField(default='Test', max_length=50, verbose_name='Model'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='odo',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Odo reading'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='other',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Other Accessories'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='perdate',
            field=models.DateField(blank=True, null=True, verbose_name='Permit expiry'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='perfile',
            field=models.FileField(blank=True, default='', null=True, upload_to='media', verbose_name='Permit File'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='perno',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Permit number'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='poldate',
            field=models.DateField(blank=True, null=True, verbose_name='Pollution Expiry'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='polfile',
            field=models.FileField(blank=True, default='', null=True, upload_to='media', verbose_name='Pollution File'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='polno',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Pollution number'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='postatus',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='pstatus',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='reg',
            field=models.FileField(blank=True, null=True, upload_to='media', verbose_name='Registratrion file'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='region',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Region'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='size',
            field=models.CharField(default='Test', max_length=15, verbose_name='Vehicle size'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='status',
            field=models.IntegerField(choices=[(1, 'Available'), (2, 'Unavailable'), (3, 'Trip assigned'), (4, 'On trip'), (5, 'Loading'), (6, 'Unloading')], default=2, verbose_name='Vehicle status'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='taxdate',
            field=models.DateField(blank=True, null=True, verbose_name='Tax Expiry'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='taxfile',
            field=models.FileField(blank=True, default='', null=True, upload_to='media', verbose_name='Tax File'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='taxno',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Tax number'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='tstatus',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='tyreno',
            field=models.IntegerField(blank=True, default=4, null=True, verbose_name='No. of Tyres'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='veh',
            field=models.CharField(default='test', max_length=30, verbose_name='Vehicle number'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='welfrdate',
            field=models.DateField(blank=True, null=True, verbose_name='Welfare Expiry'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='welfrfile',
            field=models.FileField(blank=True, default='', null=True, upload_to='media', verbose_name='Welfare File'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='welfrno',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Welfare number'),
        ),
        migrations.AddField(
            model_name='vehiclemaster',
            name='wstatus',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterModelTable(
            name='vehiclecategory',
            table=None,
        ),
    ]
