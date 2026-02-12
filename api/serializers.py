from rest_framework import serializers
from .models import SailorUser,Course,Category,Module,video_contents,docs_contents
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
        data.pop('refresh', None)
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
        fields = ['name', 'category', 'description']

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
        fields = ['name', 'course']
        
        
class video_contentsSerializer(serializers.ModelSerializer):
        module = serializers.SlugRelatedField(
            slug_field='name',
            queryset=Module.objects.all()
        )
        class Meta:
            model = video_contents
            fields = ['module', 'title', 'video_file']
        
class docs_contentsSerializer(serializers.ModelSerializer):
    module = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Module.objects.all()
    )
    class Meta:
        model = docs_contents
        fields = ['module', 'title', 'doc_file']
        
