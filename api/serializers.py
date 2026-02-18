from rest_framework import serializers
from .models import SailorUser,Course,Category,Module,video_contents,docs_contents,Video_Activity,Soar_Quiz_Average_Score,Soar_Category,Soar_Quiz_Data,Soar_Quiz_Answer  
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class SailorUserSerializer(serializers.ModelSerializer):
    email = serializers.SlugRelatedField(
        slug_field = 'email',
        queryset = User.objects.all()
    )
    class Meta:                                                                                             
        model = SailorUser
        fields = ['id', 'email', 'name', 'age', 'rank', 'mobile_number', 'address']
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        try:
            sailor = SailorUser.objects.get(email=user)

            
            token['email'] = user.email
            token['is_verified'] = sailor.is_verified

        except SailorUser.DoesNotExist:
            pass

        return token

    def validate(self, attrs):
        data = super().validate(attrs)


        sailor = SailorUser.objects.get(email=self.user)
        # if not sailor.is_verified:
        #     raise serializers.ValidationError("Email not verified")
        #     data['user'] = {
        #     "id": self.user.id,
        #     "email": self.user.email,
        #     "name": sailor.name,
        #     "is_verified": sailor.is_verified
        # }
        return data

class CourseSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Category.objects.all()
    )
    class Meta:
        model = Course
        fields = ['id','name', 'category', 'description']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
        
class ModuleSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Course.objects.all()
    )
    class Meta:
        model = Module
        fields = ['id','name', 'course']
        
        
class video_contentsSerializer(serializers.ModelSerializer):
        module = serializers.SlugRelatedField(
            slug_field='name',
            queryset=Module.objects.all()
        )
        class Meta:
            model = video_contents
            fields = ['id','module', 'title', 'video_file']
        
class docs_contentsSerializer(serializers.ModelSerializer):
    module = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Module.objects.all()
    )
    class Meta:
        model = docs_contents
        fields = ['id','module', 'title', 'doc_file']
        
class video_activitySerializer(serializers.ModelSerializer):
    video = serializers.SlugRelatedField(
        slug_field='title',
        queryset=video_contents.objects.all()
    )
    class Meta:
        model = Video_Activity
        fields = ['id','video', 'activity_time', 'type']
        
class Soar_CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Soar_Category
        fields = '__all__'
        
class Soar_Quiz_DataSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Soar_Category.objects.all()
    )
    class Meta:
        model = Soar_Quiz_Data
        fields = ['id','category', 'question', 'option_a', 'option_b', 'option_c', 'option_d']
        
class Soar_Quiz_AnswerSerializer(serializers.ModelSerializer):
     quiz_data = serializers.SlugRelatedField(
            slug_field='question',
            queryset=Soar_Quiz_Data.objects.all()
        )
     SailorUser = serializers.SlugRelatedField(
            slug_field='email',queryset = SailorUser.objects.all(),source='email.email')
     
     category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Soar_Category.objects.all()
    )
     class Meta:
            model = Soar_Quiz_Answer
            fields = ['id','quiz_data','category','selected_option','SailorUser', 'points']
        
class Soar_Quiz_Average_ScoreSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Soar_Category.objects.all()
    )
    SailorUser = serializers.SlugRelatedField(
        slug_field='email',
        queryset=SailorUser.objects.all()
    )
    class Meta:
        model = Soar_Quiz_Average_Score
        fields = ['id','SailorUser','category', 'average_score']
         