# Generated by Django 4.0.1 on 2022-06-19 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginmodule', '0009_patient_health_detail_countt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient_health_detail',
            name='paid_original',
            field=models.IntegerField(default=0),
        ),
    ]