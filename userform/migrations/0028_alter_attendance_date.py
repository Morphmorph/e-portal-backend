# Generated by Django 4.2.7 on 2024-05-22 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userform', '0027_alter_attendance_enrollment_alter_attendance_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(),
        ),
    ]
