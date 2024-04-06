# models.py

from django.db import models

class Student(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    studentID = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    middleName = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    contactNumber = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    gradeLevel = models.IntegerField()
    section = models.CharField(max_length=100)
    adviser = models.CharField(max_length=100)
    dob = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    userType = models.CharField(max_length=20, default='student')  # New field for user type

class Parents(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, related_name='parents', on_delete=models.CASCADE)
    mothersName = models.CharField(max_length=100)
    mothersContact = models.CharField(max_length=100)
    mothersOccupation = models.CharField(max_length=100)
    m_dob = models.DateField()
    m_age = models.IntegerField()
    fathersName = models.CharField(max_length=100)
    fathersContact = models.CharField(max_length=100)
    fathersOccupation = models.CharField(max_length=100)
    f_dob = models.DateField()
    f_age = models.IntegerField()

class Teacher(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    employeeID = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    middleName = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    contactNumber = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    dob = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    gradeLevel = models.IntegerField()
    section = models.CharField(max_length=100)
    userType = models.CharField(max_length=20, default='teacher')  # New field for user type

class AcademicData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    teacher = models.OneToOneField(Teacher, related_name='academic_data', on_delete=models.CASCADE)
    lastSchoolAttended = models.CharField(max_length=255)
    schoolAddress = models.CharField(max_length=255)
    yearGraduated = models.IntegerField()
    degree = models.CharField(max_length=100)
    achievements = models.TextField()
    prcNumber = models.CharField(max_length=100)
    expirationDate = models.DateField()
    yearsOfTeaching = models.IntegerField()
