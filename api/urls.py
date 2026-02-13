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
   path('modules/',views.ModuleList.as_view(),name='module list create'),
    path('create_module/',views.create_module,name='create module'),
    path('module/<int:module_id>/',views.get_module_details,name='module detail'),
    path('update_module/<int:module_id>/',views.update_module,name='update module'),
    path('delete_module/<int:module_id>/',views.delete_module,name='delete module'),

    
    
    ############################
    ####### video contents API URLS ######
    ############################
    path('video_contents/',views.video_content_list.as_view(),name='video contents list create'),
    path('create_video_content/',views.Create_video_content,name='create video content'),
    path('video_content/<int:video_content_id>/',views.get_video_content_details,name='video content detail'),
    path('update_video_content/<int:video_content_id>/',views.update_video_content,name='update video content'),
    path('delete_video_content/<int:video_content_id>/',views.delete_video_content,name='delete video content'),
   


    ############################
    ####### docs contents API URLS ######
    ############################
    path('docs_contents/',views.docs_content_list.as_view(),name='docs contents list create'),
    path('create_docs_content/',views.Create_docs_content,name='create docs content'),
    path('docs_content/<int:docs_content_id>/',views.get_details_docs_content,name='docs content detail'),
    path('update_docs_content/<int:docs_content_id>/',views.update_docs_content,name
='update docs content'),
    path('delete_docs_content/<int:docs_content_id>/',views.delete_docs_content,name='delete docs content'),    
    
    
############################################
############# API for Overall course Details
############################################
path('over_all_course_details/',views.get_overall_course_details,name='course details'),

]

