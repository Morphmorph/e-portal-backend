# serializers.py

from rest_framework import serializers
from .models import Student, Parents, Teacher, AcademicData

class ParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents
        fields = '__all__'

class AcademicDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicData
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    parents = ParentsSerializer()
    
    class Meta:
        model = Student
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    academic_data = AcademicDataSerializer()
    
    class Meta:
        model = Teacher
        fields = '__all__'
