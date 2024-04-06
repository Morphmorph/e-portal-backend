from django.db import models

class Parent(models.Model):
    userType = models.CharField(max_length=10)
    mothersName = models.CharField(max_length=100)
    mothersContact = models.CharField(max_length=20)
    mothersOccupation = models.CharField(max_length=100)
    mothersAddress = models.TextField()
    m_dob = models.DateField()
    m_age = models.IntegerField()
    fathersName = models.CharField(max_length=100)
    fathersContact = models.CharField(max_length=20)
    fathersOccupation = models.CharField(max_length=100)
    fathersAddress = models.TextField()
    f_dob = models.DateField()
    f_age = models.IntegerField()

class AcademicData(models.Model):
    userType = models.CharField(max_length=10)
    lastSchoolAttended = models.CharField(max_length=100)
    schoolAddress = models.TextField()
    yearGraduated = models.IntegerField()  # Assuming this is required
    degree = models.CharField(max_length=100)
    achievements = models.TextField()  # You can adjust this field based on your requirements
    prcNumber = models.CharField(max_length=20)
    expirationDate = models.DateField()
    yearsOfTeaching = models.IntegerField()

class Student(models.Model):
    userType = models.CharField(max_length=10)
    studentID = models.CharField(max_length=20)
    lastName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    middleName = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    contactNumber = models.CharField(max_length=20)
    address = models.TextField()
    dob = models.DateField(null=True)  # Nullable field
    age = models.IntegerField(null=True)  # Nullable field
    gender = models.CharField(max_length=10, null=True)
    gradeLevel = models.IntegerField(null=True)  # Nullable field
    section = models.CharField(max_length=20, null=True)
    adviser = models.CharField(max_length=100, null=True)
    parents = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True)  # Make parents field nullable
    academicData = models.ForeignKey(AcademicData, on_delete=models.CASCADE, null=True)  # Make academicData field nullable

class Teacher(models.Model):
    userType = models.CharField(max_length=10)
    employeeID = models.CharField(max_length=20)
    lastName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    middleName = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    contactNumber = models.CharField(max_length=20)
    address = models.TextField()
    dob = models.DateField(null=True)  # Nullable field
    age = models.IntegerField(null=True)  # Nullable field
    gender = models.CharField(max_length=10, null=True)
    gradeLevel = models.IntegerField(null=True)  # Nullable field
    section = models.CharField(max_length=20, null=True)
    academicData = models.ForeignKey(AcademicData, on_delete=models.CASCADE, null=True)  # Make academicData field nullable
