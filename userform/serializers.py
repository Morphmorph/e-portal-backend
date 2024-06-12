from rest_framework import serializers
from .models import Student, Teacher, Parent, Academic, SectionHandle, User, Enrollment, SubjectHandle, Attendance, Section, Grade
from rest_framework import serializers
from django.contrib.auth import authenticate

class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        fields = '__all__'

    def validate_studentID(self, value):
        if Student.objects.filter(studentID=value).exists():
            raise serializers.ValidationError('Student already exists.')
        return value

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
        
    def validate_employeeID(self, value):
        if Teacher.objects.filter(employeeID=value).exists():
            raise serializers.ValidationError('Teacher already exists.')
        return value    

class AcademicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academic
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['name', 'id']
        
class SectionHandleSerializer(serializers.ModelSerializer):
    section_name = serializers.CharField(source='section.name', read_only=True)
    class Meta:
        model = SectionHandle
        fields = '__all__'
        
class SubjectHandleSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.name')
    class Meta:
        model = SubjectHandle
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
        
class AttendanceSerializer(serializers.ModelSerializer):
    enrollment = EnrollmentSerializer()
    class Meta:
        model = Attendance
        fields = ['student', 'status', 'enrollment', 'date', 'status']

class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # To handle password
    
    class Meta:
        model = User
        fields = ['username', 'password']  # Add more fields if needed

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            # Add more fields here if needed
        )
        return user
    
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'