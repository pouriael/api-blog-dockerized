from rest_framework import serializers
from django.contrib.auth.models import User
from dataclasses import fields
from tkinter.ttk import Style
from xml.dom import ValidationErr
from rest_framework import serializers

from .utils import Util
from .models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

#def clean_email(value):
#    if 'admin' in value:
#        raise serializers.ValidationError('admin cant be in email') 
#    return value
#
#class UserRegisterSerializer(serializers.ModelSerializer):
#    password2 = serializers.CharField(write_only =True,required=True)
#    class Meta:
#        model = User
#        fields =[
#            'email',
#            'name',
#            'password',
#            'password2',
#            'tc',
#        ]
#        extra_kwargs = {
#            'password': {'write_only':True},
#            'email':{'validators':[clean_email]}
#            }
#
#    def create(self,validated_data):
#        del validated_data['password2']
#        return User.objects.create_user(**validated_data)
#
#    def validate_username(self,value):
#        if value == 'admin':
#            raise serializers.ValidationError("user name cant be admin")
#        return value
#
#    def validate(self,data):
#        if data['password'] != data['password2']:
#            raise serializers.ValidationError('passwords must match')
#        return data
#
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'




class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only = True)
    class Meta:
        model = User
        fields =[
            'email',
            'name',
            'password',
            'password2',
            'tc',
        ]
        extra_kwargs = {
            'password': {'write_only':True}
        }
    
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password2 !=password:
            raise serializers.ValidationError('Password and confirm Password doesnt match')
        return attrs

    def create(self,validate_data):
       return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length =255)
    class Meta:
        model = User
        fields =[
            'email',
            'password',
        ]
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'email',
            'name',
         ]

class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = [
            'password',
            'password2',
        ]
    
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password2 !=password:
            raise serializers.ValidationError('Password and confirm Password doesnt match')
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        fields = ['email']

    def validate(self,attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("encoded UID", uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('passsword reset token',token)
            link ='http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('password reset link',link)
            # Send Email
            body = 'Click Follwing Link to Reset Your Password' + link
            data = {
                'subject':'Reset Your Password',
                'body': body,
                'to_email':user.email,
            }
            Util.send_email(data)
            return attrs
        else:
            raise ValidationErr("you are not a Registred User")
        


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields = [
            'password',
            'password2',
        ]
    
    def validate(self,attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password2 !=password:
                raise serializers.ValidationError('Password and confirm Password doesnt match')
            id = str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationErr('Token is not valid or expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationErr('Token is not valid or expired ')
            