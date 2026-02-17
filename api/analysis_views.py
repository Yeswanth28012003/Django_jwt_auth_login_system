from  rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .models import (
    SailorUser,
    Course,
    Category,
    Module,
    video_contents,
    docs_contents,
    Video_Activity,
    BaseModel
    
    
    )
from .serializers import (SailorUserSerializer,
MyTokenObtainPairSerializer,
CourseSerializer,
CategorySerializer,
ModuleSerializer,
video_contentsSerializer,
docs_contentsSerializer,
video_activitySerializer


                )

from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.mail import EmailMessage,send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from .otpgenerstor import generate_otp
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated





