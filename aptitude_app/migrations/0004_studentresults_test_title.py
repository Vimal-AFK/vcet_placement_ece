# Generated by Django 5.1.4 on 2025-02-08 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aptitude_app', '0003_globalsettings_delete_extra'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentresults',
            name='test_title',
            field=models.CharField(default='', max_length=255),
        ),
    ]
