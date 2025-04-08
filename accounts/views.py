from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import SendOTPSerializer, VerifyOTPSerializer
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
import random


def generate_otp():
    return str(random.randint(100000, 999999))


class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        
        user, created = User.objects.get_or_create(phone=phone)
        otp = generate_otp()
        user.otp_code = otp
        user.otp_created_at = timezone.now()
        user.save()
        
        print(f"OTP (demo): {otp}")  

        return Response({'detail': 'OTP sent successfully'})


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        otp = serializer.validated_data['otp']

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=404)

        if user.otp_code != otp:
            return Response({'detail': 'Invalid OTP'}, status=400)

        if timezone.now() - user.otp_created_at > timedelta(minutes=5):
            return Response({'detail': 'OTP expired'}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
