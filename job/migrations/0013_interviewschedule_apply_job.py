# Generated by Django 3.2.16 on 2023-07-17 02:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0012_chatmessage_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='interviewschedule',
            name='apply_job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='job.applyjob'),
        ),
    ]
