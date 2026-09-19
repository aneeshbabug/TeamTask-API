from django.http import HttpResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response

from .serializer import UserRegisterSerializer, UserSerializer
from .models import User

from drf_spectacular.utils import extend_schema

# Create your views here.
def home(request):
    return HttpResponse('Welcome to TeamTask API')


class Register(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        request=UserRegisterSerializer,
        responses={201: None},
        auth=[],
    )
    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message':'User Created Successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


