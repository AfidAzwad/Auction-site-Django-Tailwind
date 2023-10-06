from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .emails import send_activation_email
from .serializers import UserSerializer
import jwt
from django.conf import settings
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken



class LoginAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            user = authenticate(request, username=data['email'], password=data['password'])
            if not user:
                return Response({'message': 'Wrong credentials!'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if not user.is_active:
                return Response({'message': 'Please activate user with activation link to login!'}, status=status.HTTP_401_UNAUTHORIZED)
            
            login(request, user)
            refresh_token = RefreshToken.for_user(user)
            response = Response()
            response.set_cookie(key='refresh_token', 
                                value=str(refresh_token),
                                httponly=True)
            response.data = {
                'token': str(refresh_token.access_token)
                    }
            return response
        except Exception as e:
            return Response({'message': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RegisterAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(email=serializer.data['email'])
                user.set_password(data['password'])
                user.is_active = False
                user.save()
                send_activation_email(request, user)
                response_dict = {
                        'status': 200,
                        'message': 'Registration successfull! check email',
                        'data': serializer.data,
                    }
                return Response(response_dict)
            response_dict = {
                'status': 400,
                'message': 'Something went wrong !',
                'data': serializer.errors,
            }
            return Response(response_dict)
        except Exception as e:
            return e


class AccountActivateView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            if decoded_token['user_id'] == user.id:
                if user.is_active:
                    return Response({'message': 'Your account has been already activated.'}, status=status.HTTP_400_BAD_REQUEST)

                user.is_active = True
                user.save()
                return Response({'message': 'Your account has been activated successfully.'}, status=status.HTTP_200_OK)

            return Response({'error': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, jwt.ExpiredSignatureError):
            return Response({'error': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)
        