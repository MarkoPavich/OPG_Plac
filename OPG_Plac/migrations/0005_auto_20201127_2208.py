# Generated by Django 3.1 on 2020-11-27 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OPG_Plac', '0004_auto_20201127_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcategory',
            name='position_index',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='position_index',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productsubcategory',
            name='position_index',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
