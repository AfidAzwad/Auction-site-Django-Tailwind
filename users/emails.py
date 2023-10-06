from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from .utils import generate_jwt_token
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


def send_activation_email(request, user):
    token = generate_jwt_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request).domain
    mail_subject = "Activate your account"
    
    activation_link = f"http://{current_site}/api/user/activate/{uid}/{token}/"
    
    subject = "Activate your account"
    message = f"Dear {user.username},\n\nPlease click the link below to activate your account:\n{activation_link}\n\nBest regards,\nAuction Team"
    to_email = user.email
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [to_email])
    
    return Response({'message': 'Activation email sent successfully'}, status=status.HTTP_200_OK)