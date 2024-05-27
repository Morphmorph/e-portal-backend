from django.db import models
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver


class Section(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SectionHandle(models.Model):
    created_at = models.DateTimeField()
    teacher = models.OneToOneField('Teacher', related_name='section_handle_rel', on_delete=models.CASCADE, unique=True)
    grade_level = models.CharField(max_length=50)
    section = models.ForeignKey(Section, related_name='section_handles', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.teacher} - {self.grade_level} - {self.section}"
    
    def save(self, *args, **kwargs):
        if not self.created_at:  # Populate created_at if not provided
            self.created_at = timezone.now() + timedelta(hours=8)  # Adjust by adding 8 hours
        super().save(*args, **kwargs)   
        
class Parent(models.Model):
    created_at = models.DateTimeField()
    mothersName = models.CharField(max_length=100)
    mothersContact = models.CharField(max_length=100)
    mothersOccupation = models.CharField(max_length=100)
    m_dob = models.DateField(null=True)
    m_age = models.IntegerField(null=True)
    fathersName = models.CharField(max_length=100)
    fathersContact = models.CharField(max_length=100)
    fathersOccupation = models.CharField(max_length=100)
    f_dob = models.DateField(null=True)
    f_age = models.IntegerField(null=True)
    
    def save(self, *args, **kwargs):
        if not self.id:  # Only adjust the created_at value if it's a new instance
            self.created_at = timezone.now() + timedelta(hours=8)  # Adjust by adding 8 hours
        super().save(*args, **kwargs)

class Student(models.Model):
    created_at = models.DateTimeField()
    studentID = models.CharField(max_length=100, unique=True)
    lastName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    middleName = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    address = models.TextField()
    gradeLevel = models.CharField(max_length=100, null=True)
    dob = models.DateField(null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=10)
    parent = models.ForeignKey(Parent, related_name='students', on_delete=models.SET_NULL, null=True)
    # Add enrollment relationship
    section_handles = models.ManyToManyField('SectionHandle', through='Enrollment')
    
    def save(self, *args, **kwargs):
        if not self.id:  # Only adjust the created_at value if it's a new instance
            self.created_at = timezone.now() + timedelta(hours=8)  # Adjust by adding 8 hours
            self.password = make_password(self.password)  # Encrypt password
        super().save(*args, **kwargs)
        # Create corresponding User instance after saving the Student
        if not self.user:  # Check if User instance doesn't exist
            User.objects.create(role='student', student=self)

class Academic(models.Model):
    created_at = models.DateTimeField()
    lastSchoolAttended = models.CharField(max_length=100)
    schoolAddress = models.TextField()
    yearGraduated = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    prcNumber = models.CharField(max_length=100)
    expirationDate = models.DateField(null=True)
    yearsOfTeaching = models.CharField(max_length=100)
        
    def save(self, *args, **kwargs):
        if not self.id:  # Only adjust the created_at value if it's a new instance
            self.created_at = timezone.now() + timedelta(hours=8)  # Adjust by adding 8 hours
        super().save(*args, **kwargs)
   
class Teacher(models.Model):
    created_at = models.DateTimeField()
    employeeID = models.CharField(max_length=100, unique=True)
    lastName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    middleName = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    contactNumber = models.CharField(max_length=100)
    address = models.TextField()
    dob = models.DateField(null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=10)
    academic = models.ForeignKey(Academic, related_name='teachers', on_delete=models.SET_NULL, null=True)
    
    # Add a related name for the section handle relationship
    section_handle = models.OneToOneField(SectionHandle, related_name='teacher_rel', on_delete=models.CASCADE, null=True)
    
    def save(self, *args, **kwargs):
        if not self.id:  # Only adjust the created_at value if it's a new instance
            self.created_at = timezone.now() + timedelta(hours=8)  # Adjust by adding 8 hours
            self.password = make_password(self.password)  # Encrypt password
        super().save(*args, **kwargs)
        # Create corresponding User instance after saving the Teacher
        if not hasattr(self, 'user'):  # Check if User instance doesn't exist
            User.objects.create(role='teacher', teacher=self)

    def add_student_to_section(self, student, section_handle):
        Enrollment.objects.create(student=student, section=section_handle)

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SubjectHandle(models.Model):
    created_at = models.DateTimeField()
    teacher = models.ForeignKey('Teacher', related_name='subject_handles', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='subject_handles', on_delete=models.CASCADE)
    grade_level = models.CharField(max_length=50)
    section = models.ForeignKey(Section, related_name='subject_handles', on_delete=models.CASCADE)
    time_in = models.TimeField()
    time_out = models.TimeField()

    def save(self, *args, **kwargs):
        if not self.created_at:  # Populate created_at if not provided
            self.created_at = timezone.now() + timedelta(hours=8)  # Adjust by adding 8 hours
        super().save(*args, **kwargs)
    class Meta:
        # Add a unique constraint on the combination of teacher and subject fields
        unique_together = ('teacher', 'subject')

class Enrollment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, related_name='enrollments', on_delete=models.CASCADE)
    section = models.ForeignKey(SectionHandle, related_name='enrollments', on_delete=models.CASCADE)
    
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=20)

    class Meta:
        unique_together = ('student', 'enrollment', 'date')

    def __str__(self):
        return f"{self.student} - {self.enrollment.section} - {self.date} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.date:  # Populate date if not provided
            self.date = (timezone.now() + timedelta(hours=8)).date()  # Adjust by adding 8 hours
        super().save(*args, **kwargs)
        
class User(models.Model):
    ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher')
    )
    created_at = models.DateTimeField()
    role = models.CharField(max_length=20, choices=ROLES)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, null=True, blank=True)
            
    def save(self, *args, **kwargs):
        if not self.id:  # Only adjust the created_at value if it's a new instance
            self.created_at = timezone.now() + timedelta(hours=8)  # Adjust by adding 8 hours
        super().save(*args, **kwargs)

@receiver(post_save, sender=Student)
def create_student_user(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'user'):  # Check if User instance doesn't exist
        User.objects.create(role='student', student=instance)

@receiver(post_save, sender=Teacher)
def create_teacher_user(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'user'):  # Check if User instance doesn't exist
        User.objects.create(role='teacher', teacher=instance)
