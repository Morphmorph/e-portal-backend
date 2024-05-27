# Generated by Django 4.2.7 on 2024-05-08 01:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userform', '0004_alter_enrollment_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectHandle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('grade_level', models.CharField(max_length=50)),
                ('section', models.CharField(max_length=50)),
                ('time_in', models.TimeField()),
                ('time_out', models.TimeField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_handles', to='userform.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_handles', to='userform.teacher')),
            ],
        ),
    ]
