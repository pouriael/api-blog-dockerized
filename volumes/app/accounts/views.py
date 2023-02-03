from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import generics
from .models import *
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle

#Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#class UserRegister(APIView):
#    throttle_classes = [AnonRateThrottle,UserRateThrottle]
#    renderer_classes = [UserRenderer]
#    def post(self,request):
#        ser_data = UserRegisterSerializer(data=request.POST)
#        if ser_data.is_valid():
#            ser_data.create(ser_data.validated_data)
#            user = ser_data.save()
#            token=get_tokens_for_user(user)
#            return Response({'token':token,'msg': 'Registration Successful'},status=status.HTTP_201_CREATED)
#        return Response(ser_data.errors,status = status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ViewSet):
    permission_classess = [IsAuthenticated]
    queryset = User.objects.all()

    def list(self,request):
        srz_data = UserSerializer(instance=self.queryset,many=True)
        return Response(data=srz_data.data)

    def retrieve(self,request,pk=None):
        user = get_object_or_404(self,pk=pk)
        srz_data = UserSerializer(instance=user)
        return Response(data = srz_data.data)

    def partial_update(self,request,pk=None):
        user = get_object_or_404(self.queryset,pk=pk)
        srz_data = UserSerializer(instance=user,data=request.POST,partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data)
        return Response(data=srz_data.errors)

    def destroy(self,request,pk=None):
        user = get_object_or_404(self.queryset,pk=pk)
        user.is_active = False
        user.save()
        return Response({'message':'user deactivated'})


class UserRegistrationView(APIView):
    throttle_classes = [AnonRateThrottle,UserRateThrottle]
    renderer_classes = [UserRenderer]
    def post(self, request,format=None):
        serializer = UserRegistrationSerializer(data =request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg': 'Registration Successful'},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class UserLoginView(APIView):
    throttle_classes = [UserRateThrottle]
    renderer_classes = [UserRenderer]
    def post(self, request,format=None):
        serializer = UserLoginSerializer(data =request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            print(email)
            password = serializer.data.get('password')
            print(password)
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg': 'Login Successful'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    throttle_classes=[UserRateThrottle]
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = UserChangePasswordSerializer(data =request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Change successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = SendPasswordResetEmailSerializer(data =request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password reset link sent please check email'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView(APIView):
    renderer_classes =[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer = UserPasswordResetSerializer(data =request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Change successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)