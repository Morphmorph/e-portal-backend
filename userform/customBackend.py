from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .models import Student, Teacher

class StudentTeacherAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        User = get_user_model()
        
        # Check if the username exists in Student or Teacher
        student = Student.objects.filter(studentID=username).first()
        teacher = Teacher.objects.filter(employeeID=username).first()

        if student:
            if password == student.password:  # Compare passwords directly
                role = 'student'
                return student
            else:
                return None

        elif teacher:
            if password == teacher.password:  # Compare passwords directly
                role = 'teacher'
                return teacher
            else:
                return None

        else:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
