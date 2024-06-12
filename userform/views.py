from django.http import HttpResponseBadRequest, JsonResponse
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import StudentSerializer, TeacherSerializer, ParentSerializer, AcademicSerializer, SectionHandleSerializer, GradeSerializer, SubjectHandleSerializer, LoginSerializer, EnrollmentSerializer, AttendanceSerializer
from .models import Student, Teacher, Parent, Academic, SectionHandle, User, Enrollment, Subject, SubjectHandle, Attendance, Section, Grade
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import render, get_object_or_404
import logging
import json
from django.utils import timezone
from datetime import timedelta
from datetime import datetime


# Get an instance of a logger
logger = logging.getLogger(__name__)

@api_view(['POST'])
def register_user(request):
    role = request.data.get('role')
    if role == 'student':
        # Code for student registration
        student_serializer = StudentSerializer(data=request.data)
        parent_serializer = ParentSerializer(data=request.data.get('parents'))
        if student_serializer.is_valid() and parent_serializer.is_valid():
            # Check if the student already exists
            request.data['password'] = make_password(request.data['password'])
            student_id = request.data.get('studentID')
            if Student.objects.filter(studentID=student_id).exists():
                return Response({'error': 'Student already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            parent_instance = parent_serializer.save()
            student_instance = student_serializer.save(parent=parent_instance)
            return Response({'message': 'Student registered successfully'})
        else:
            student_errors = student_serializer.errors if not student_serializer.is_valid() else {}
            parent_errors = parent_serializer.errors if not parent_serializer.is_valid() else {}
            errors = {**student_errors, **parent_errors}
            return Response(errors, status=400)

    elif role == 'teacher':
        # Code for teacher registration
        teacher_serializer = TeacherSerializer(data=request.data)
        academic_data = request.data.pop('academic', None)  # Remove academic data from request data
        if teacher_serializer.is_valid():
            # Check if the teacher already exists
            request.data['password'] = make_password(request.data['password'])
            teacher_id = request.data.get('employeeID')
            if Teacher.objects.filter(employeeID=teacher_id).exists():
                return Response({'error': 'Teacher already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            teacher_instance = teacher_serializer.save()
            
            # Process academic data separately
            if academic_data:
                academic_serializer = AcademicSerializer(data=academic_data)
                if academic_serializer.is_valid():
                    academic_instance = academic_serializer.save()
                    teacher_instance.academic = academic_instance
                    teacher_instance.save()
                    return Response({'message': 'Teacher registered successfully'})
                else:
                    return Response({'error': 'Error processing academic data.'}, status=status.HTTP_400_BAD_REQUEST)  # Include appropriate error message
            else:
                return Response({'error': 'Academic data is required for teacher registration.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Error validating teacher data.'}, status=status.HTTP_400_BAD_REQUEST)  # Include appropriate error message

    else:
        return HttpResponseBadRequest("Invalid role")


@api_view(['POST'])
def add_section_handles(request):
    teacher_id = request.data.get('teacher_id')
    grade_level = request.data.get('grade_level')
    section_name = request.data.get('section')
    
    if not teacher_id or not grade_level or not section_name:
        return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)
    
    teacher = Teacher.objects.filter(id=teacher_id).first()
    if not teacher:
        return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if the teacher already has a section handle
    existing_section_handle = SectionHandle.objects.filter(teacher=teacher).first()
    if existing_section_handle:
        return Response({'error': 'Teacher already handles a section'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the section already has a teacher assigned
    existing_section_handle_for_section = SectionHandle.objects.filter(section__name=section_name).first()
    if existing_section_handle_for_section:
        return Response({'error': 'Section already assigned to a teacher'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        section, created = Section.objects.get_or_create(name=section_name)
        if created:
            SectionHandle.objects.create(teacher=teacher, grade_level=grade_level, section=section)
            return Response({'message': 'Section handle added successfully'})
        else:
            return Response({'error': 'Section already exists and is assigned to a teacher'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_section_handles(request):
    try:
        section_handles = SectionHandle.objects.all()
        serialized_data = []
        
        for section_handle in section_handles:
            # Serialize section handle data
            section_handle_serializer = SectionHandleSerializer(section_handle)
            serialized_section_handle = section_handle_serializer.data
            
            # Get teacher data
            teacher_id = section_handle.teacher_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_serializer = TeacherSerializer(teacher)
            teacher_data = teacher_serializer.data
            
            # Add teacher data to serialized section handle
            serialized_section_handle['teacher'] = teacher_data
            
            serialized_data.append(serialized_section_handle)
        
        return Response(serialized_data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_subject_handle(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            teacher_id = data.get('teacher')
            subject_name = data.get('subject')
            grade_level = data.get('grade_level')
            section_name = data.get('section')
            time_in = data.get('time_in')
            time_out = data.get('time_out')

            if not (teacher_id and subject_name and grade_level and section_name and time_in and time_out):
                return JsonResponse({'success': False, 'error': 'All fields are required.'}, status=400)

            teacher = Teacher.objects.filter(pk=teacher_id).first()
            subject, created = Subject.objects.get_or_create(name=subject_name)  # Get or create the subject object
            section = Section.objects.filter(name=section_name).first()

            if not teacher:
                return JsonResponse({'success': False, 'error': 'Teacher matching query does not exist.'}, status=400)
            if not subject:
                return JsonResponse({'success': False, 'error': 'Subject matching query does not exist.'}, status=400)
            if not section:
                return JsonResponse({'success': False, 'error': 'Section matching query does not exist.'}, status=400)
            
            # Check if the subject in the section already has a teacher assigned
            existing_subject_handle = SubjectHandle.objects.filter(
                subject=subject,
                section=section
            ).first()
            if existing_subject_handle:
                return JsonResponse({'success': False, 'error': 'A teacher is already assigned to this subject in this section.'}, status=400)
            
            # Check if the teacher already handles the subject in the specified section
            existing_subject_handle = SubjectHandle.objects.filter(
                teacher=teacher,
                subject=subject,
                section=section
            ).first()
            if existing_subject_handle:
                return JsonResponse({'success': False, 'error': 'This teacher already handles this subject in this section.'}, status=400)

            subject_handle = SubjectHandle.objects.create(
                teacher=teacher,
                subject=subject,
                grade_level=grade_level,
                section=section,  # Assign the Section instance
                time_in=time_in,
                time_out=time_out
            )
            return JsonResponse({'success': True, 'subject_handle_id': subject_handle.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format in request body.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
@api_view(['GET'])
def get_subject_handles(request):
    try:
        subject_handles = SubjectHandle.objects.all()
        serialized_data = []

        for subject_handle in subject_handles:
            # Serialize subject handle data
            subject_handle_serializer = SubjectHandleSerializer(subject_handle)
            serialized_subject_handle = subject_handle_serializer.data
            
            # Get teacher data
            teacher_id = subject_handle.teacher_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_serializer = TeacherSerializer(teacher)
            teacher_data = teacher_serializer.data
            
            # Replace section ID with section name
            section_name = subject_handle.section.name
            
            # Add teacher data and section name to serialized subject handle
            serialized_subject_handle['teacher'] = teacher_data
            serialized_subject_handle['section'] = section_name
            
            serialized_data.append(serialized_subject_handle)

        return Response(serialized_data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_teacher_sections(request, teacher_id):
    try:
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
    
    section_handles = SectionHandle.objects.filter(teacher=teacher)
    if not section_handles.exists():
        return Response([], status=status.HTTP_200_OK)

    serializer = SectionHandleSerializer(section_handles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_users(request):
    students = Student.objects.all()
    teachers = Teacher.objects.all()

    # Serialize parent data for students
    student_data = []
    for student in students:
        student_serializer = StudentSerializer(student)
        parent_serializer = ParentSerializer(student.parent)
        student_data.append({
            'student': student_serializer.data,
            'parent': parent_serializer.data
        })

    # Serialize academic data for teachers
    teacher_data = []
    for teacher in teachers:
        teacher_serializer = TeacherSerializer(teacher)
        academic_serializer = AcademicSerializer(teacher.academic)
        teacher_data.append({
            'teacher': teacher_serializer.data,
            'academic': academic_serializer.data
        })

    return Response({
        'students': student_data,
        'teachers': teacher_data,
    })
    
class TeacherList(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            # Check if the username exists in Student or Teacher
            student = Student.objects.filter(studentID=username).first()
            teacher = Teacher.objects.filter(employeeID=username).first()

            if student:
                if check_password(password, student.password):
                    role = 'student'
                    user_id = student.id  # Get the ID of the student
                    return Response({'message': 'Login successful', 'role': role, 'user_id': user_id})
                else:
                    return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

            elif teacher:
                if check_password(password, teacher.password):
                    role = 'teacher'
                    user_id = teacher.id  # Get the ID of the teacher
                    return Response({'message': 'Login successful', 'role': role, 'user_id': user_id})
                else:
                    return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the provided credentials match the hardcoded admin credentials
            elif username == 'cocsadmin' and password == 'cocs1955':
                # Hardcoded admin credentials
                admin_id = 1010203  # You can set the admin user ID as needed
                return Response({'message': 'Admin login successful', 'role': 'admin', 'user_id': admin_id})

            else:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_user_data(request, username):
    try:
        # Check if the user is a student
        student = Student.objects.filter(studentID=username).select_related('parent').first()
        if student:
            # Serialize student and related data
            serialized_data = {
                'user_id': student.id,
                'role': 'student',
                'student_id': student.studentID,
                'name': f"{student.lastName}, {student.firstName} {student.middleName}",
                'address': student.address,
                'grade_level': student.gradeLevel,
                'dob': student.dob,
                'age': student.age,
                'gender': student.gender,
                'parent': {
                    'mothersName': student.parent.mothersName,
                    'mothersContact': student.parent.mothersContact,
                    'mothersOccupation': student.parent.mothersOccupation,
                    'm_dob': student.parent.m_dob,
                    'm_age': student.parent.m_age,
                    'fathersName': student.parent.fathersName,
                    'fathersContact': student.parent.fathersContact,
                    'fathersOccupation': student.parent.fathersOccupation,
                    'f_dob': student.parent.f_dob,
                    'f_age': student.parent.f_age,
                }
            }
            # Check if the student is enrolled in a section
            if hasattr(student, 'enrollments'):
                enrolled_sections = [enrollment.section for enrollment in student.enrollments.all()]
                serialized_data['enrolled_sections'] = SectionHandleSerializer(enrolled_sections, many=True).data
            return JsonResponse(serialized_data, status=200)

        # If not a student, check if the user is a teacher
        teacher = Teacher.objects.filter(employeeID=username).select_related('academic').first()
        if teacher:
            # Serialize teacher and related data
            serialized_data = {
                'user_id': teacher.id,
                'role': 'teacher',
                'employee_id': teacher.employeeID,
                'name': f"{teacher.lastName}, {teacher.firstName} {teacher.middleName}",
                'contactNumber': teacher.contactNumber,
                'address': teacher.address,
                'dob': teacher.dob,
                'age': teacher.age,
                'gender': teacher.gender,
                'academic': {
                    'lastSchoolAttended': teacher.academic.lastSchoolAttended,
                    'schoolAddress': teacher.academic.schoolAddress,
                    'yearGraduated': teacher.academic.yearGraduated,
                    'degree': teacher.academic.degree,
                    'prcNumber': teacher.academic.prcNumber,
                    'expirationDate': teacher.academic.expirationDate,
                    'yearsOfTeaching': teacher.academic.yearsOfTeaching,
                }
            }
            # Get section handles associated with the teacher
            section_handles = SectionHandle.objects.filter(teacher=teacher)
            serialized_section_handles = [SectionHandleSerializer(handle).data for handle in section_handles]
            serialized_data['section_handles'] = serialized_section_handles
            
            # Get subject handles associated with the teacher
            subject_handles = SubjectHandle.objects.filter(teacher=teacher)
            serialized_subject_handles = [SubjectHandleSerializer(handle).data for handle in subject_handles]
            serialized_data['subject_handles'] = serialized_subject_handles
            
            return JsonResponse(serialized_data, status=200)

        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def get_students_by_grade_level(request):
    if request.method == 'GET':
        grade_level = request.GET.get('grade_level')
        without_section = request.GET.get('without_section', False)  # Default to False if not provided

        if grade_level:
            students = Student.objects.filter(gradeLevel=grade_level)
            if without_section:
                # Exclude students who are already enrolled in a section
                enrolled_student_ids = Enrollment.objects.filter(student_id__in=students.values_list('id', flat=True)).values_list('student_id', flat=True)
                students = students.exclude(id__in=enrolled_student_ids)
                
            serialized_students = StudentSerializer(students, many=True)
            return JsonResponse({'students': serialized_students.data}, status=200)
        else:
            return JsonResponse({'error': 'Grade level parameter is required'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@api_view(['POST'])
def add_student_to_section(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            section_handle_id = data.get('section_handle_id')

            if not (student_id and section_handle_id):
                return JsonResponse({'success': False, 'error': 'Both student_id and section_handle_id are required.'}, status=400)

            student = Student.objects.filter(pk=student_id).first()
            section_handle = SectionHandle.objects.filter(pk=section_handle_id).first()

            if not student:
                return JsonResponse({'success': False, 'error': 'Student matching query does not exist.'}, status=400)
            if not section_handle:
                return JsonResponse({'success': False, 'error': 'Section handle matching query does not exist.'}, status=400)

            if Enrollment.objects.filter(student=student, section=section_handle).exists():
                return JsonResponse({'success': False, 'error': 'Student is already enrolled in this section.'}, status=400)

            Enrollment.objects.create(student=student, section=section_handle)
            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format in request body.'}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
@api_view(['GET'])
def get_enrolled_students(request, section_handle_id):
    if request.method == 'GET':
        try:
            # Retrieve enrolled students for the specified section handle id
            enrolled_students = Enrollment.objects.filter(section_id=section_handle_id)

            # Serialize enrolled students data
            serialized_data = []
            for student_enrollment in enrolled_students:
                # Fetch additional data related to the student
                student = student_enrollment.student
                section_handle = student_enrollment.section
                section = section_handle.section  # Access the Section object through SectionHandle
                student_data = {
                    'user_id': student.id,
                    'role': 'student',
                    'student_id': student.studentID,
                    'name': f"{student.firstName} {student.middleName} {student.lastName}",
                    'address': student.address,
                    'grade_level': student.gradeLevel,
                    'dob': student.dob,
                    'age': student.age,
                    'gender': student.gender,
                    'parent': {
                        'mothersName': student.parent.mothersName,
                        'mothersContact': student.parent.mothersContact,
                        'mothersOccupation': student.parent.mothersOccupation,
                        'm_dob': student.parent.m_dob,
                        'm_age': student.parent.m_age,
                        'fathersName': student.parent.fathersName,
                        'fathersContact': student.parent.fathersContact,
                        'fathersOccupation': student.parent.fathersOccupation,
                        'f_dob': student.parent.f_dob,
                        'f_age': student.parent.f_age,
                    }
                }
                # Include the section data
                section_data = {
                    'section_id': section.id,
                    'section_name': section.name,
                    'section_grade_level': section_handle.grade_level,
                    'section_teacher': {
                        'teacher_id': section_handle.teacher.id,
                        'teacher_name': f"{section_handle.teacher.firstName} {section_handle.teacher.middleName} {section_handle.teacher.lastName}",
                    } if section_handle.teacher else None,
                }
                # Include the additional data along with enrollment data
                enrollment_data = EnrollmentSerializer(student_enrollment).data
                enrollment_data['student'] = student_data
                enrollment_data['section'] = section_data
                serialized_data.append(enrollment_data)

            return JsonResponse({'students': serialized_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@api_view(['GET'])
def get_teachers_with_subject_handles(request, teacher_id):
    if request.method == 'GET':
        try:
            # Check if the teacher has any subject handles
            if SubjectHandle.objects.filter(teacher_id=teacher_id).exists():
                # Retrieve subject handles for the specified teacher_id
                subject_handles = SubjectHandle.objects.filter(teacher_id=teacher_id)
                
                # Serialize subject handles data with section names and IDs
                serialized_data = []
                for subject_handle in subject_handles:
                    serialized_handle = {
                        'id': subject_handle.id,
                        'teacher': subject_handle.teacher.id,
                        'subject': subject_handle.subject.name,
                        'subject_id': subject_handle.subject.id,
                        'grade_level': subject_handle.grade_level,
                        'section_id': subject_handle.section.id,  # Include section ID
                        'section': subject_handle.section.name,  # Retrieve section name
                        'time_in': subject_handle.time_in,
                        'time_out': subject_handle.time_out
                    }
                    serialized_data.append(serialized_handle)
                
                return JsonResponse(serialized_data, status=200, safe=False)
            else:
                return JsonResponse({'message': 'This teacher does not have any subject handles.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@api_view(['POST'])
def update_student_attendance(request):
    student_id = request.data.get('student_id')
    section_handle_id = request.data.get('section_id')
    status_data = request.data.get('status')
    date = request.data.get('date', timezone.now().date())  # Optional date parameter, default to today

    if not student_id or not status_data or not section_handle_id:
        return Response({'error': 'student_id, section_handle_id, and status are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        student = Student.objects.get(id=student_id)
        section_handle = SectionHandle.objects.get(id=section_handle_id)
        enrollment = Enrollment.objects.get(student=student, section=section_handle)

        # Retrieve the student's grade level
        grade_level = student.gradeLevel

        attendance, created = Attendance.objects.update_or_create(
            student=student,
            enrollment=enrollment,
            date=date,
            defaults={'status': status_data, 'grade_level': grade_level}  # Include grade level when saving attendance
        )
        if created:
            message = 'New attendance record created'
        else:
            message = 'Attendance updated successfully'
        return Response({'message': message}, status=status.HTTP_200_OK)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    except SectionHandle.DoesNotExist:
        return Response({'error': 'Section handle not found'}, status=status.HTTP_404_NOT_FOUND)
    except Enrollment.DoesNotExist:
        return Response({'error': 'Enrollment not found for the given student and section'}, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['GET'])
def get_student_attendance(request, student_id=None):
    if student_id:
        try:
            attendance_records = Attendance.objects.filter(student_id=student_id)
            if not attendance_records.exists():
                return Response({'error': 'Attendance data not found for the specified student'}, status=status.HTTP_404_NOT_FOUND)
            serializer = AttendanceSerializer(attendance_records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        attendance_records = Attendance.objects.all()
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def get_students_attendance(request, student_id):
    if student_id:
        try:
            attendance_records = Attendance.objects.filter(student_id=student_id)
            if not attendance_records.exists():
                return Response({'error': 'Attendance data not found for the specified student'}, status=status.HTTP_404_NOT_FOUND)
            serializer = AttendanceSerializer(attendance_records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        attendance_records = Attendance.objects.all()
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def get_enrolled_students_by_section(request, section_id):
    if request.method == 'GET':
        try:
            # Retrieve enrolled students for the specified section ID
            enrolled_students = Enrollment.objects.filter(section_id=section_id)
            
            # Serialize enrolled students data
            serialized_data = []
            for student_enrollment in enrolled_students:
                # Fetch additional data related to the student
                student = student_enrollment.student
                section_handle = student_enrollment.section
                section = section_handle.section  # Access the Section object through SectionHandle
                
                student_data = {
                    'user_id': student.id,
                    'role': 'student',
                    'student_id': student.studentID,
                    'name': f"{student.firstName} {student.middleName} {student.lastName}",
                    'address': student.address,
                    'grade_level': student.gradeLevel,
                    'dob': student.dob,
                    'age': student.age,
                    'gender': student.gender,
                    'parent': {
                        'mothersName': student.parent.mothersName,
                        'mothersContact': student.parent.mothersContact,
                        'mothersOccupation': student.parent.mothersOccupation,
                        'm_dob': student.parent.m_dob,
                        'm_age': student.parent.m_age,
                        'fathersName': student.parent.fathersName,
                        'fathersContact': student.parent.fathersContact,
                        'fathersOccupation': student.parent.fathersOccupation,
                        'f_dob': student.parent.f_dob,
                        'f_age': student.parent.f_age,
                    }
                }
                
                # Include the section data
                section_data = {
                    'section_id': section.id,
                    'section_name': section.name,
                    'section_grade_level': section_handle.grade_level,
                    'section_teacher': {
                        'teacher_id': section_handle.teacher.id if section_handle.teacher else None,
                        'teacher_name': f"{section_handle.teacher.firstName} {section_handle.teacher.middleName} {section_handle.teacher.lastName}" if section_handle.teacher else None,
                    }
                }
                
                # Include the additional data along with enrollment data
                enrollment_data = EnrollmentSerializer(student_enrollment).data
                enrollment_data['student'] = student_data
                enrollment_data['section'] = section_data
                serialized_data.append(enrollment_data)
                
            return JsonResponse({'students': serialized_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
@api_view(['POST'])
def add_grade(request):
    if request.method == 'POST':
        try:
            student_id = request.data.get('student')
            subject_handle_id = request.data.get('subject_handle')
            grading_period = request.data.get('grading_period')

            # Check if a grade already exists for the given student, subject handle, and grading period
            existing_grade = Grade.objects.filter(student_id=student_id, subject_handle_id=subject_handle_id, grading_period=grading_period).first()
            if existing_grade:
                # If a grade already exists, you can update the existing grade or reject the request
                # For simplicity, let's reject the request if a grade already exists
                return Response({'error': 'A grade already exists for this student in this grading'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the student's grade level
            student = Student.objects.get(id=student_id)
            grade_level = student.gradeLevel

            serializer = GradeSerializer(data=request.data)
            if serializer.is_valid():
                # Include grade level when saving grade
                serializer.save(grade_level=grade_level)
                return Response({'error': 'Grade added successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def get_student_grades(request, student_id, grade_level):
    try:
        # Retrieve the student object
        student = Student.objects.get(id=student_id)
        
        # Filter grades by student and grade level
        grades = Grade.objects.filter(student=student, grade_level=grade_level)
        
        # Serialize the grades
        serialized_grades = []
        for grade in grades:
            serialized_grade = {
                'id': grade.id,
                'grading_period': grade.grading_period,
                'grade': grade.grade,
                'subject_name': grade.subject_handle.subject.name,
            }
            serialized_grades.append(serialized_grade)
        
        return Response({'success': True, 'grades': serialized_grades}, status=status.HTTP_200_OK)
    except Student.DoesNotExist:
        return Response({'error': f'Student with ID {student_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_students_grades(request, student_id):
    subject_handle_id = request.query_params.get('subject_handle_id', None)
    grading_period = request.query_params.get('grading_period', None)
    try:
        grades = Grade.objects.filter(student_id=student_id)
        if subject_handle_id:
            grades = grades.filter(subject_handle_id=subject_handle_id)
        if grading_period:
            grades = grades.filter(grading_period=grading_period)
        
        grades = grades.select_related('subject_handle__subject')
        
        if grades.exists():
            serialized_grades = []
            for grade in grades:
                serialized_grade = {
                    'id': grade.id,
                    'grading_period': grade.grading_period,
                    'grade': grade.grade,
                    'subject_name': grade.subject_handle.subject.name,
                }
                serialized_grades.append(serialized_grade)
            return Response({'success': True, 'grades': serialized_grades}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': 'No grades found for this student'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@transaction.atomic
def promote_student_grade_level(request, student_id):
    try:
        # Retrieve the student object
        student = Student.objects.get(id=student_id)

        # Determine the new grade level based on the current grade level
        current_grade_level = student.gradeLevel
        if current_grade_level.lower() == "kinder":
            new_grade_level = "Grade 1"
        else:
            new_grade_level = f"Grade {int(current_grade_level.split()[1]) + 1}"  # Increment the grade level

        # Update the student's grade level
        student.gradeLevel = new_grade_level
        student.save()

        # Remove the student from their current section
        student_enrollments = student.enrollments.all()
        for enrollment in student_enrollments:
            enrollment.delete()

        return Response({'success': True, 'message': f'Student {student_id} grade level promoted to {new_grade_level}'}, status=status.HTTP_200_OK)
    except Student.DoesNotExist:
        return Response({'error': f'Student with ID {student_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_student_grade_levels(request, student_id):
    try:
        grades = Grade.objects.filter(student_id=student_id)
        grade_levels = grades.values_list('grade_level', flat=True).distinct()
        
        if grade_levels.exists():
            return Response({'success': True, 'grade_levels': list(grade_levels)}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': 'No grade levels found for this student'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)