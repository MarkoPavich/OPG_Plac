# Generated by Django 3.1.2 on 2020-12-22 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OPG_Plac', '0022_auto_20201222_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentoption',
            name='tooltip',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]