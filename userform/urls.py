from django.urls import path
from .views import register_user, get_users, TeacherList, add_section_handles, get_section_handles, get_students_attendance, get_enrolled_students_by_section, add_subject_handle, get_teachers_with_subject_handles, get_subject_handles, update_student_attendance, get_student_attendance, user_login, get_user_data, get_teacher_sections, get_students_by_grade_level, add_student_to_section, get_enrolled_students

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('users/', get_users, name='get_users'),
    path('login/', user_login, name='login'),
    path('get_section_handles/', get_section_handles, name='get_section_handles'),
    path('add_section_handles/', add_section_handles, name='add_section_handles'),
    path('add_subject_handle/', add_subject_handle, name='add_subject_handle'),
    path('get_subject_handles/', get_subject_handles, name='get_subject_handles'),
    path('teachers/', TeacherList.as_view(), name='teacher-list'),
    path('teachers/<int:teacher_id>/sections/', get_teacher_sections, name='teacher_sections'),
    path('user/<str:username>/', get_user_data, name='get_user_data'),
    path('get_students/', get_students_by_grade_level, name='get_students_by_grade_level'),
    path('add_student_to_section/', add_student_to_section, name='add_student_to_section'),
    path('get_enrolled_students/<int:section_handle_id>/', get_enrolled_students, name='get_enrolled_students'),
    path('teachers/<int:teacher_id>/subject_handles/', get_teachers_with_subject_handles, name='teachers_subject_handles'),
    path('sub/get_enrolled_students/<int:section_id>/', get_enrolled_students_by_section, name='get_enrolled_students_by_section'),
    path('attendance/update/', update_student_attendance, name='update_student_attendance'),
    path('attendance/<int:student_id>/', get_students_attendance, name='get_student_attendance'),
    path('attendance/', get_student_attendance, name='get_all_attendance'),
    # Other URL patterns...
    
]
