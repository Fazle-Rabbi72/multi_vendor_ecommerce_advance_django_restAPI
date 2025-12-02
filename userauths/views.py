from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
from userauths.models import User,Profile
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny

from userauths.serializer import RegisterSerializer,MyTokenObtainPairSerializer,UserSerializer,ProfileSerializer

import shortuuid



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    


class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    permission_classes=(AllowAny,)
    serializer_class=RegisterSerializer

def generate_otp():
    uuid_key=shortuuid.uuid()
    unique_key=uuid_key[:6]
    return unique_key
    
class PasswordRestEmailVerify(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    throttle_scope = 'password_reset'

    def get_object(self):
        email = self.kwargs['email']
        user = User.objects.get(email=email)

        if user:
            user.otp = generate_otp()
            user.save()

            uidb64 = user.pk
            otp = user.otp

            Link = f"http://localhost:5173/create-new-password?otp={otp}&uidb64={uidb64}"
            

           
            subject = "Password Reset Link"
            message = f"Your OTP is: {otp}\n\nClick the link to reset your password:\n{Link}"
            email_from = settings.EMAIL_HOST_USER
            recipient = [email]

            send_mail(subject, message, email_from, recipient)
            

        return user

class PasswordChangeView(generics.CreateAPIView):
    permission_classes=(AllowAny,)
    serializer_class=UserSerializer
    
    def create(self, request, *args, **kwargs):
        payload = request.data
        otp=payload['otp']
        uidb64=payload['uidb64']
        password=payload['password']
        
        user = User.objects.get(id=uidb64, otp=otp)
        if user:
            user.set_password(password)
            user.otp=""
            user.save()
            return Response({"massage":"Password changed Successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"massage":"User Does not exist"},status=status.HTTP_404_NOT_FOUND)

class ProfileView(generics.RetrieveAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[AllowAny]
    
    def get_object(self):
        user_id=self.kwargs['user_id']
        
        user=User.objects.get(id=user_id)
        profile=Profile.objects.get(user=user)
        return profile
        