# Generated by Django 4.0.1 on 2022-05-24 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginmodule', '0005_alter_account_patient_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='id',
        ),
        migrations.AlterField(
            model_name='account',
            name='patient_id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]