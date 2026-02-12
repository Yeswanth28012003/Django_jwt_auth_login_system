from django.contrib import admin
from django.urls import path 
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView






urlpatterns = [
    path('login/',views.MyTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('google-login/',views.GoogleLoginView.as_view(), name='google-login'),
    path('userlist/',views.sailoruserlistview.as_view(),name='userlist'),
    path('register/',views.signup_user,name = 'signup user'),
    # path('loginuser/',views.login_user,name = 'login user'),
    path('verify/',views.verify_email,name = "verify email"),
    path('resend_otp/',views.resend_otp,name="resend otp"),
    
    
    
    
    
    
    
    #CATEGORY API URLS
    path('create_category/',views.create_category,name='create category'),
    path('categorieslist/', views.CategoryListView.as_view() ,name='category list'),
    path('category/<int:category_id>/',views.get_category_details,name='category detail'),
    path('update_category/<int:category_id>/',views.update_category,name='update category'),
    path('delete_category/<int:category_id>/',views.delete_category,name='delete category'),
    
    
    
    
    
    
    ##### ##### #####
    # COURSE  API URLS
path('courses/',views.courlistseview.as_view(),name='course list create'),
    path('create_course/',views.Create_course,name='create course'),
    path('course/<int:course_id>/',views.get_course_details,name='course detail'),
    path('updatecourse/<int:course_id>/',views.update_course,name='update course'),
    path('deletecourse/<int:course_id>/',views.delete_course,name='delete course'),



   ############  ###########
   ##### Module API URLS####
   ############ ###########


   




]

