from rest_framework import serializers
from .models import Student, Parent, Teacher, AcademicData


class AcademicDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicData
        fields = '__all__'


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    parents = ParentSerializer()
    academicData = AcademicDataSerializer()

    class Meta:
        model = Student
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    academicData = AcademicDataSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'


class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ('academicData', 'parents')


class TeacherCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        exclude = ('academicData',)