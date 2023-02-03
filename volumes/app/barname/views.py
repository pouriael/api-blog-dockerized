from django.shortcuts import render
from rest_framework.views import APIView
from .permissions import *
from .serializers import QuestionSerializer
from .models import *
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

class barname(APIView):
    throttle_classes = [AnonRateThrottle,UserRateThrottle]
    
    def get(self, request):
        questions = Question.objects.all()
        srz_data = QuestionSerializer(instance=questions,many = True).data
        return Response(srz_data,status = status.HTTP_200_OK)

class barnamecreate(APIView):

    def post(self,request):
        srz_data = QuestionSerializer(data =request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data,status=status.HTTP_200_OK)

class barnameupdate(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def put(self,request,pk):
        question = Question.objects.get(pk=pk)
        srz_data =QuestionSerializer(instance = question,data=request.data,partial= True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data,status=status.HTTP_200_OK)
        return Response(srz_data.errors,status=status.HTTP_400_BAD_REQUEST)

class barnamedelete(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    
    def delete(self,request,pk):
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response({'message': 'question deleted'},status=status.HTTP_200_OK)