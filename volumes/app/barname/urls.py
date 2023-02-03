from django.urls import path
from . import views

app_name = 'barname'

urlpatterns = [
    path('',views.barname.as_view(),name='barname'),
    path('create/',views.barnamecreate.as_view(),name='barnamecreate'),
    path('update/<int:pk>',views.barnameupdate.as_view(),name='barnameupdate'),
    path('delete/<int:pk>',views.barnamedelete.as_view(),name='barnamedelete'),


]