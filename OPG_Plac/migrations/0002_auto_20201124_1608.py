# Generated by Django 3.1.2 on 2020-11-24 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OPG_Plac', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogarticle',
            old_name='Title image',
            new_name='title_image',
        ),
    ]
