# Generated by Django 3.1 on 2020-12-09 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OPG_Plac', '0007_auto_20201208_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]