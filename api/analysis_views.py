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
def create_quiz_answer_data(request):
    answers = request.data   
    if not isinstance(answers, list):
        return Response({"error": "Expected list of answers"}, status=400)
    created_answers = []
    try:
        for answer in answers:
            email = answer.get("email")
            category = answer.get("category")
            quiz_data = answer.get("quiz_data")
            selected_option = answer.get("selected_option")
            points = answer.get("points")
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": f"User not found: {email}"}, status=404)
            try:
                sailor_user = SailorUser.objects.get(email=user)
            except SailorUser.DoesNotExist:
                return Response({"error": "SailorUser not found"}, status=404)
            try:
                category_instance = Soar_Category.objects.get(name=category)
            except Soar_Category.DoesNotExist:
                return Response({"error": f"Category not found: {category}"}, status=404)
            try:
                quiz_data_instance = Soar_Quiz_Data.objects.get(question=quiz_data)
            except Soar_Quiz_Data.DoesNotExist:
                return Response({"error": f"Question not found: {quiz_data}"}, status=404)
            previous_attempt = Soar_Quiz_Answer.active_objects.filter(
                SailorUser=sailor_user,
                quiz_data=quiz_data_instance
            ).order_by('-attempt').first()
            new_attempt = previous_attempt.attempt + 1 if previous_attempt else 1
            Soar_Quiz_Answer.active_objects.create(
                SailorUser=sailor_user,
                category=category_instance,
                quiz_data=quiz_data_instance,
                selected_option=selected_option,
                points=points,
                attempt=new_attempt
            )
            created_answers.append({
                "question": quiz_data,
                "attempt": new_attempt
            })
        return Response({
            "msg": "All answers submitted successfully",
            "total": len(created_answers),
            "data": created_answers
        }, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=500)





    
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
    































