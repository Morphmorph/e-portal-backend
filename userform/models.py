# models.py
from django.db import models

class User(models.Model):
    USER_TYPES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    userType = models.CharField(max_length=10, choices=USER_TYPES)
    lastName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    middleName = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    contactNumber = models.CharField(max_length=20)
    address = models.TextField()
    dob = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    # Add other common fields here

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

class Student(User):
    studentID = models.CharField(max_length=100)
    gradeLevel = models.IntegerField(null=True, blank=True)
    section = models.CharField(max_length=50)
    adviser = models.CharField(max_length=100)
    mothersName = models.CharField(max_length=100)
    mothersContact = models.CharField(max_length=20)
    mothersOccupation = models.CharField(max_length=100)
    m_dob = models.DateField(null=True, blank=True)
    m_age = models.IntegerField(null=True, blank=True)
    fathersName = models.CharField(max_length=100)
    fathersContact = models.CharField(max_length=20)
    fathersOccupation = models.CharField(max_length=100)
    f_dob = models.DateField(null=True, blank=True)
    f_age = models.IntegerField(null=True, blank=True)
    # Add other fields specific to students

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

class Teacher(User):
    employeeID = models.CharField(max_length=100)
    gradeLevel = models.IntegerField(null=True, blank=True)
    section = models.CharField(max_length=50)
    lastSchoolAttended = models.CharField(max_length=100)
    schoolAddress = models.TextField()
    yearGraduated = models.IntegerField(null=True, blank=True)
    degree = models.CharField(max_length=100)
    prcNumber = models.CharField(max_length=100)
    expirationDate = models.DateField(null=True, blank=True)
    yearsOfTeaching = models.IntegerField(null=True, blank=True)
    # Add other fields specific to teachers

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
