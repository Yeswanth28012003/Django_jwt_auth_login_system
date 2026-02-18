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
    Soar_Category,
    Soar_Quiz_Data,
    Soar_Quiz_Answer,
    Soar_Quiz_Average_Score
    
    
    
    )
from .serializers import (SailorUserSerializer,
MyTokenObtainPairSerializer,
CourseSerializer,
CategorySerializer,
ModuleSerializer,
video_contentsSerializer,
docs_contentsSerializer,
video_activitySerializer,
Soar_CategorySerializer,
Soar_Quiz_DataSerializer,
Soar_Quiz_AnswerSerializer,
Soar_Quiz_Average_ScoreSerializer



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
from rest_framework import viewsets 

##########################################################
########## SOAR CARD CATEGORY API VIEWS ################### ###########################################################


class Soar_CategoryViewSet(viewsets.ModelViewSet):
    queryset = Soar_Category.objects.all()
    serializer_class = Soar_CategorySerializer
    permission_classes = [AllowAny]
    
##########################################################
########## SOAR QUIZ DATA API VIEWS ################### ###########################################################

class Soar_Quiz_DataViewSet(viewsets.ModelViewSet):
    queryset = Soar_Quiz_Data.objects.all()
    serializer_class = Soar_Quiz_DataSerializer
    permission_classes = [AllowAny]
    

@api_view(['POST'])
@permission_classes([AllowAny])
def create_quiz_answer_data_calculation(request):
    serializer = Soar_Quiz_AnswerSerializer(data=request.data)
    if serializer.is_valid():
        quiz_answer = serializer.save()
        print("Quiz answer saved:", quiz_answer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)











    
##########################################################
########## SOAR QUIZ ANSWER API VIEWS ################### ###########################################################

class Soar_Quiz_AnswerViewSet(viewsets.ModelViewSet):
    queryset = Soar_Quiz_Answer.objects.all()
    serializer_class = Soar_Quiz_AnswerSerializer
    permission_classes = [AllowAny]
    






    

##########################################################
########## SOAR QUIZ AVERAGE SCORE API VIEWS ################### ###########################################################
class Soar_Quiz_Average_ScoreViewSet(viewsets.ModelViewSet):
    queryset = Soar_Quiz_Average_Score.objects.all()
    serializer_class = Soar_Quiz_Average_ScoreSerializer
    permission_classes = [AllowAny]
    































