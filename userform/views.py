from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student, Teacher
from .serializers import StudentSerializer, TeacherSerializer

@api_view(['GET', 'POST'])
def create_user(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = StudentSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        userType = request.data.get('userType')
        if userType == 'student':
            serializer = StudentSerializer(data=request.data)
        elif userType == 'teacher':
            serializer = TeacherSerializer(data=request.data)
        else:
            return Response({'error': 'Invalid userType'}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
