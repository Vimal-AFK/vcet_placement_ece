# Generated by Django 5.1.4 on 2025-01-18 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aptitude_app', '0002_alter_batch_options_remove_batch_unique_batch_year_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='year',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
