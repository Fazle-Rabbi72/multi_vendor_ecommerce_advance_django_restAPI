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
from rest_framework_simplejwt.tokens import RefreshToken

from userauths.serializer import RegisterSerializer,MyTokenObtainPairSerializer,UserSerializer,ProfileSerializer

import shortuuid
import random


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    


class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    permission_classes=(AllowAny,)
    serializer_class=RegisterSerializer

def generate_numeric_otp(length=7):
        # Generate a random 7-digit OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
        return otp
    
class PasswordRestEmailVerify(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    throttle_scope = 'password_reset'

    def get_object(self):
        email = self.kwargs['email']
        user = User.objects.get(email=email)

        if user:
            user.otp = generate_numeric_otp()
            uidb64 = user.pk
            
             # Generate a token and include it in the reset link sent via email
            refresh = RefreshToken.for_user(user)
            reset_token = str(refresh.access_token)

            # Store the reset_token in the user model for later verification
            user.reset_token = reset_token
            user.save()

            Link = f"http://localhost:5173/create-new-password?otp={user.otp}&uidb64={uidb64}&reset_token={reset_token}"
            

           
            subject = "Password Reset Link"
            message = f"Click the link to reset your password:\n{Link}"
            email_from = settings.EMAIL_HOST_USER
            recipient = [email]

            send_mail(subject, message, email_from, recipient)
            

        return user

class PasswordChangeView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    throttle_scope='password_change'
    
    def create(self, request, *args, **kwargs):
        payload = request.data
        
        otp = payload['otp']
        uidb64 = payload['uidb64']
        reset_token = payload['reset_token']
        password = payload['password']


        user = User.objects.get(id=uidb64, otp=otp)
        if user:
            user.set_password(password)
            user.otp = ""
            user.reset_token = ""
            user.save()

            
            return Response( {"message": "Password Changed Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response( {"message": "An Error Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProfileView(generics.RetrieveAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[AllowAny]
    
    def get_object(self):
        user_id=self.kwargs['user_id']
        
        user=User.objects.get(id=user_id)
        profile=Profile.objects.get(user=user)
        return profile
        