# Generated by Django 4.0.1 on 2022-06-14 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginmodule', '0008_remove_patient_detail_blood_group_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient_health_detail',
            name='countt',
            field=models.TextField(default=0, max_length=20),
        ),
        migrations.AddField(
            model_name='patient_health_detail',
            name='m_time',
            field=models.TextField(default=0, max_length=30),
        ),
        migrations.AddField(
            model_name='patient_health_detail',
            name='note',
            field=models.TextField(default=0, max_length=30),
        ),
    ]
