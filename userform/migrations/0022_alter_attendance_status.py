# Generated by Django 4.2.7 on 2024-05-20 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userform', '0021_alter_attendance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent')], max_length=10),
        ),
    ]
