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
    Video_Activity
    
    
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
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage,send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import authenticate
from .otpgenerstor import generate_otp
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("id_token")

        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            "404596195032-7qe88v9d7soicdvmkt640i497e838gah.apps.googleusercontent.com"
        )

        email = idinfo["email"]

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": email}
        )

   
        SailorUser.objects.get_or_create(email=user)
        sailor_user = SailorUser.objects.get(email=user)
        print(sailor_user)
        sailor_user.is_google_auth = True
        sailor_user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })

class sailoruserlistview(generics.ListCreateAPIView):
    queryset = SailorUser.objects.all()
    serializer_class = SailorUserSerializer
    permission_classes = [IsAuthenticated]
    
# Sign up User View
# @csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        user.save()
        sailor_user = SailorUser.objects.create(email=user)
        sailor_user.otp = generate_otp()
        sailor_user.otp_created_at = timezone.now()
        sailor_user.save()
        send_mail(
            subject="Verify Your Otp",
            message=f"Your otp is {sailor_user.otp}", 
            from_email= settings.EMAIL_HOST_USER,
            recipient_list=[sailor_user.email.email],
            fail_silently=False
        )
        return Response(
            {'message': 'User created successfully. Please verify your email.'},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        print(e)
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def resend_otp(request):
    email = request.data.get("email")

    try:
        user = User.objects.get(email=email)
        sailor_user = SailorUser.objects.get(email=user)
    except User.DoesNotExist:
        return Response({"msg": "User not found"}, status=404)
    except SailorUser.DoesNotExist:
        return Response({"msg":"Sailor use not found"},status=404)

    if sailor_user.is_verified:
        return Response({"msg": "User already verified"}, status=400)


    if sailor_user.otp_created_at and timezone.now() < sailor_user.otp_created_at + timedelta(minutes=1):
        return Response({"msg": "Please wait before requesting new OTP"}, status=400)
    
    sailor_user.otp = generate_otp()
    sailor_user.otp_created_at = timezone.now()
    sailor_user.save()

    send_mail(
        subject="Resend OTP",
        message=f"Your new OTP is {sailor_user.otp}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )

    return Response({"msg": "New OTP sent successfully"}, status=200)

#Normal Login View
# @csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, username=email, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        try:
            sailor_obj = SailorUser.objects.get(email=user)
            if sailor_obj.is_verified:
                return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'email': user.email,
                    'name': sailor_obj.name,
                }
                        })
            else:
                return Response({"error":"user is not verified correctly pls again signUp"},status=404)
        except SailorUser.DoesNotExist:
            return Response({"error":"user is removed"},status=404)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    email = request.data.get("email")
    otp = request.data.get("otp")
    print(email)
    try:
        user = User.objects.get(email=email)
        sailor_user = SailorUser.objects.get(email=user)
    except User.DoesNotExist  :
        return Response({"msg":"user not found"},status=404)
    except SailorUser.DoesNotExist:
        return Response({"msg":"User Not Found "},status=404)
    if sailor_user.otp != otp:
        return Response({"msg":"Invalid OTP"},status=400)
    if timezone.now() > sailor_user.otp_created_at + timedelta(minutes=5):
        return Response({"msg":"OTP expired"},status=400)
    sailor_user.is_verified = True
    sailor_user.otp = None
    sailor_user.save()
    return Response({"message":"Email verfied Successfully"},status=200)

##############################################################################################################################################################
##################### CATEGORY API VIEWS ##################################### ###############################################################################
##############################################################################################################################################################
@api_view(['POST'])
@permission_classes([AllowAny])
def create_category(request):
    serializer = CategorySerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
@permission_classes([AllowAny])
def get_category_details(request, category_id):
    try:
        category_obj =  serializer = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"msg":"Category Not Found"},status=404)
    serializer = CategorySerializer(category_obj)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([AllowAny])
def update_category(request, category_id):
    try:
        category_obj = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"msg":"Category Not Found"},status=404)
    serializer = CategorySerializer(category_obj, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_category(request, category_id):
    try:
        category_obj = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"msg":"Category Not Found"},status=404)
    category_obj.delete()
    return Response({"msg":"Category Deleted Successfully"},status=204)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

################################################################################################################################################################
########### Course API Views ################################################## ###############################################################################
###############################################################################################################################################################
@api_view(['POST'])
@permission_classes([AllowAny])
def Create_course(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class courlistseview(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

# class courseviewdetails(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#     permission_classes = [IsAuthenticated]

@api_view(['GET'])
@permission_classes([AllowAny])
def get_course_details(request, course_id):
    try:
        course = Course.objects.get(id = course_id)
    except Course.DoesNotExist: 
        return Response({"msg":"Course NOt found"},status=404)
    serializer  = CourseSerializer(course)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([AllowAny])
def update_course(request,course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"msg":"Course Not Found"},status=404)
    serializer = CourseSerializer(course, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"msg":"Course Not Found"},status=404)
    course.delete()
    return Response({"msg":"Course Deleted Successfully"},status=204)


##############################################################################################
########## MODULE API VIEWS ###############################################################
#############################################################################################

@api_view(['POST'])
@permission_classes([AllowAny])
def create_module(request):
    serializer = ModuleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_module_details(request, module_id):
    try:
        module_obj =  Module.objects.get(id=module_id)
    except Module.DoesNotExist:
        return Response({"msg":"Module Not Found"},status=404)
    serializer = ModuleSerializer(module_obj)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([AllowAny])
def update_module(request, module_id):
    try:
        module_obj = Module.objects.get(id=module_id)
    except Module.DoesNotExist:
        return Response({"msg":"Module Not Found"},status=404)
    serializer = ModuleSerializer(module_obj, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_module(request, module_id):
    try:
        module_obj = Module.objects.get(id=module_id)
    except Module.DoesNotExist:
        return Response({"msg":"Module Not Found"},status=404)
    module_obj.delete()
    return Response({"msg":"Module Deleted Successfully"},status=204)

class ModuleList(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [AllowAny]


###################################################################################################################   VIDEO CONTENTS API VIEWS  ###################################################################################################################
@api_view(['POST'])
@permission_classes([AllowAny])
def Create_video_content(request):
    serializer = video_contentsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_video_content_details(request , video_id):
    try:
        video_obj = video_contents.objects.get(id=video_id)
    except video_contents.DoesNotExist:
        return Response({"msg":"Video Content Not Found"},status=404)
    serializer = video_contentsSerializer(video_obj, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([AllowAny])
def update_video_content(request, video_id):
    try:
        video_obj = video_contents.objects.get(id=video_id)
    except video_contents.DoesNotExist:
        return Response({"msg":"Video Content Not Found"},status=404)
    serializer = video_contentsSerializer(video_obj, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_video_content(request, video_id):
    try:
        video_obj = video_contents.objects.get(id=video_id)
    except video_contents.DoesNotExist:
        return Response({"msg":"Video Content Not Found"},status=404)
    video_obj.delete()
    return Response({"msg":"Video Content Deleted Successfully"},status=204)


class video_content_list(generics.ListCreateAPIView):
    queryset = video_contents.objects.all()
    serializer_class = video_contentsSerializer
    permission_classes = [AllowAny]
    
    
##########################################################################################################################################
########## DOCS CONTENT API VIEWS  #######################################################################################################
##########################################################################################################################################
    
@api_view(['POST'])
@permission_classes([AllowAny])
def Create_docs_content(request):
    serializer = docs_contentsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_details_docs_content(request,docs_id):
    try:
        docs_obj = docs_contents.objects.get(id=docs_id)
    except docs_contents.DoesNotExist:
        return Response({"msg":"Docs Content Not Found"},status=404)
    serializer = docs_contentsSerializer(docs_obj, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([AllowAny])
def update_docs_content(request, docs_id):
    try:
        docs_obj = docs_contents.objects.get(id=docs_id)
    except docs_contents.DoesNotExist:
        return Response({"msg":"Docs Content Not Found"},status=404)
    serializer = docs_contentsSerializer(docs_obj, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_docs_content(request, docs_id):
    try:
        docs_obj = docs_contents.objects.get(id=docs_id)
    except docs_contents.DoesNotExist:
        return Response({"msg":"Docs Content Not Found"},status=404)
    docs_obj.delete()
    return Response({"msg":"Docs Content Deleted Successfully"},status=204)


class docs_content_list(generics.ListCreateAPIView):
    queryset = docs_contents.objects.all()
    serializer_class = docs_contentsSerializer
    permission_classes = [AllowAny]
    

################################################################################################################
################################ OVER ALL COURSE  DETAILVIEW vIEWS ################################################ ########################################################################################################################


@api_view(['GET'])
@permission_classes([AllowAny])
def get_overall_course_details(request):
    courses = Course.objects.all()
    overall_data = []

    for course_obj in courses:
        course_serializer = CourseSerializer(
            course_obj,
            context={'request': request}
        )

        modules = course_obj.modules.all()
        module_data = []

        for module in modules:
            module_serializer = ModuleSerializer(
                module,
                context={'request': request}
            )

            video_contents_qs = module.video_contents.all()
            video_data = []
            for video in video_contents_qs:
                video_serializer = video_contentsSerializer(
                    video,
                    context={'request': request}
                ).data
                
                video_activity_qs = video.activities.all()
                video_activity_data = video_activitySerializer(
                    video_activity_qs,
                    many=True,
                    context={'request': request}
                ).data
                video_data.append({
                    "video": video_serializer,
                    "activities": video_activity_data
                })
            docs_contents_qs = module.docs_contents.all()
            docs_data = docs_contentsSerializer(
                docs_contents_qs,
                many=True,
                context={'request': request}   
            ).data

            module_data.append({
                "module": module_serializer.data,
                "video_contents": video_data,
                "docs_contents": docs_data
            })

        overall_data.append({
            "course": course_serializer.data,
            "modules": module_data
        })

    return Response(overall_data, status=status.HTTP_200_OK)

###################################################################################################################
############################### ACTIVITY APIS  ###################################################################################################################

@api_view(['POST'])
@permission_classes([AllowAny])
def create_video_activity(request):
    serializer = video_activitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_video_activity_details(request, activity_id):
    try:
        activity_obj = Video_Activity.objects.get(id = activity_id)
    except Video_Activity.DoesNotExist:
        return Response({"msg":"Activity Not Found"},status=404)
    
    serializer = video_activitySerializer(activity_obj)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([AllowAny])
def update_video_activity(request, activity_id):
    try:
        activity_obj = Video_Activity.objects.get(id=activity_id)
    except Video_Activity.DoesNotExist:
        return Response({"msg":"Activity Not Found"},status=404)
    serializer = video_activitySerializer(activity_obj, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_video_activity(request, activity_id):
    try:
        activity_obj = Video_Activity.objects.get(id = activity_id)
    except Video_Activity.DoesNotExist:
        return Response({"msg":"Activity Not Found"},status=404)
    activity_obj.delete()
    return Response({"msg":"Activity Deleted Successfully"},status=204)

class VideoActivityList(generics.ListCreateAPIView):
    queryset = Video_Activity.objects.all()
    serializer_class = video_activitySerializer
    permission_classes = [AllowAny]
    
