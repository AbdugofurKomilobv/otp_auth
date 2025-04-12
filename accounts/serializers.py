from rest_framework import serializers

from .models import *

class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.CharField()

class TeacherCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'subject', 'experience_years']
