from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Teacher, Parents, AcademicData
import json

# views.py

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user_type = data.get('userType')  # Extract userType from the request payload
            if user_type == 'student':
                # Create Student object
                # Set userType field to 'student'
                student = Student.objects.create(
                    studentID=data['studentID'],
                    lastName=data['lastName'],
                    firstName=data['firstName'],
                    middleName=data['middleName'],
                    password=data['password'],
                    contactNumber=data['contactNumber'],
                    address=data['address'],
                    gradeLevel=data['gradeLevel'],
                    section=data['section'],
                    adviser=data['adviser'],
                    dob=data['dob'],
                    age=data['age'],
                    gender=data['gender'],
                    userType=user_type
                )
                # Continue with creating related objects for student
                return JsonResponse({'success': True, 'message': 'Student created successfully'}, status=201)
            elif user_type == 'teacher':
                # Create Teacher object
                # Set userType field to 'teacher'
                teacher = Teacher.objects.create(
                    employeeID=data['employeeID'],
                    lastName=data['lastName'],
                    firstName=data['firstName'],
                    middleName=data['middleName'],
                    password=data['password'],
                    contactNumber=data['contactNumber'],
                    address=data['address'],
                    dob=data['dob'],
                    age=data['age'],
                    gender=data['gender'],
                    gradeLevel=data['gradeLevel'],
                    section=data['section'],
                    userType=user_type
                )
                # Continue with creating related objects for teacher
                return JsonResponse({'success': True, 'message': 'Teacher created successfully'}, status=201)
            else:
                return JsonResponse({'error': 'Invalid user type'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
