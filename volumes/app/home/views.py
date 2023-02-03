from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from .serializers import PersonSerializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

class home(APIView):
    def get(self, request):
        persons = Person.objects.all()
        ser_data = PersonSerializers(instance=persons , many=True)
        return Response(data = ser_data.data)
    
    def post(self,request):
        name = request.data['name']
        return Response({'name':name})
