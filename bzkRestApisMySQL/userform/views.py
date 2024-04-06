from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StudentSerializer, TeacherSerializer

class UserCreateAPIView(APIView):
    def post(self, request, format=None):
        user_type = request.data.get('userType')

        if user_type == 'student':
            serializer = StudentCreateSerializer(data=request.data)
        elif user_type == 'teacher':
            serializer = TeacherCreateSerializer(data=request.data)
        else:
            return Response({'error': 'Invalid user type'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)