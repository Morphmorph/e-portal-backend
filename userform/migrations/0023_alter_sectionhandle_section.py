# Generated by Django 4.2.7 on 2024-05-20 01:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userform', '0022_alter_attendance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sectionhandle',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='section_handles', to='userform.section'),
        ),
    ]
