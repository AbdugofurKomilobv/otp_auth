from django.urls import path
from .views import SendOTPView, VerifyOTPView,CreateTeacherAPIView

urlpatterns = [
    path('send-otp/', SendOTPView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('teacher/create/', CreateTeacherAPIView.as_view(), name='teacher-create'),
]
