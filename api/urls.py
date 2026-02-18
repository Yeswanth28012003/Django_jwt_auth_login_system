from django.contrib import admin
from django.urls import path 
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import analysis_views


soar_cattegory_list = analysis_views.Soar_CategoryViewSet.as_view({
    'get':'list',
    'post':'create',
})

soar_cattegory_detail = analysis_views.Soar_CategoryViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'delete':'destroy',
})

soar_quiz_data_list = analysis_views.Soar_Quiz_DataViewSet.as_view({
    'get':'list',
    'post':'create',
})

soar_quiz_data_detail = analysis_views.Soar_Quiz_DataViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'delete':'destroy',
})

soar_quiz_answer_list =  analysis_views.Soar_Quiz_AnswerViewSet.as_view({
    'get':'list',
    'post':'create',
})

soar_quiz_answer_detail = analysis_views.Soar_Quiz_AnswerViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'delete':'destroy',
})


soar_quiz_Average_score = analysis_views.Soar_Quiz_Average_ScoreViewSet.as_view({
    'get':'list',
    'post':'create',
})

soar_quiz_Average_score_detail = analysis_views.Soar_Quiz_Average_ScoreViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'delete':'destroy',
})

















urlpatterns = [
    path('auth/login/',views.MyTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('auth/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('auth/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('auth/google-login/',views.GoogleLoginView.as_view(), name='google-login'),
    path('auth/register/',views.signup_user,name = 'signup user'),
    # path('loginuser/',views.login_user,name = 'login user'),
    path('auth/verify-account/<str:token>',views.verify_account,name = "verify email"),
    path('auth/resend_otp/',views.resend_otp,name="resend otp"),
    
    
    #############################################################################
    ######################## API URLS for FORGOT PASSWORD #######################
    #############################################################################
    path('auth/forgot',views.forgot_password,name='forgot password'),
    path('auth/set-password/<str:email>',views.reset_password,name='reset password'),
    
    
    
    #############################################################################
    ######################## API URLS for SailorUser ############################
    #############################################################################
    path('userlist/',views.sailoruserlistview.as_view(),name='userlist'),
    
    

    
    
    
    
    
    
    #################################################
    ########## CATEGORY API URLS########################
    ##################################################
    
    path('create_category/',views.create_category,name='create category'),
    path('categorieslist/', views.CategoryListView.as_view() ,name='category list'),
    path('category/<int:category_id>/',views.get_category_details,name='category detail'),
    path('update_category/<int:category_id>/',views.update_category,name='update category'),
    path('delete_category/<int:category_id>/',views.delete_category,name='delete category'),
    
    
    
    
    
    
    ##### ##### #####
    # COURSE  API URLS
    path('courses/',views.courlistseview.as_view(),name='course list create'),
    path('create_course/',views.Create_course,name='create course'),
    path('get_course/<int:course_id>/',views.get_course_details,name='course detail'),
    path('update_course/<int:course_id>/',views.update_course,name='update course'),
    path('delete_course/<int:course_id>/',views.delete_course,name='delete course'),
    ################## ########### #######
    ##### Restore APIs URL ###########
    ################# ##### ############# ##
    path('restore_course/<int:course_id>/',views.restore_course,name='restore course'),
    path('restore_module/<int:module_id>/',views.restore_module,name='restore module'),
    path('restore_video_content/<int:video_id>/',views.restore_video_content,name='restore video content'),
    path('restore_docs_content/<int:docs_id>/',views.restore_docs_content,name='restore docs content'),
    path('restore_activity/<int:activity_id>/',views.restore_video_activity,name='restore video activity'),
    
    ##########################################
    ########### GET ALL DELETED  API URLS ##########
    ##########################################
    path('get_deleted_courses/',views.get_deleted_courses,name='get deleted courses'),
    path('get_deleted_modules/',views.get_deleted_modules,name='get deleted modules'),
    path('get_deleted_video_contents/',views.get_deleted_video_contents,name='get deleted video contents'),
    path('get_deleted_docs_contents/',views.get_deleted_docs_contents,name='get deleted docs contents'),
    path('get_deleted_activities/',views.get_deleted_video_activities,name='get deleted video activities'),
    



   ############  ###########
   ##### Module API URLS####
   ############ ###########
    path('modules/',views.ModuleList.as_view(),name='module list create'),
    path('create_module/',views.create_module,name='create module'),
    path('get_module/<int:module_id>/',views.get_module_details,name='module detail'),
    path('update_module/<int:module_id>/',views.update_module,name='update module'),
    path('delete_module/<int:module_id>/',views.delete_module,name='delete module'),

    
    
    ######################################
    ####### video contents API URLS ######
    #####################################
    path('video_contents/',views.video_content_list.as_view(),name='video contents list create'),
    path('create_video_content/',views.Create_video_content,name='create video content'),
    path('get_video_content/<int:video_id>/',views.get_video_content_details,name='video content detail'),
    path('update_video_content/<int:video_id>/',views.update_video_content,name='update video content'),
    path('delete_video_content/<int:video_id>/',views.delete_video_content,name='delete video content'),



    #####################################
    ####### docs contents API URLS ######
    #####################################
    path('docs_contents/',views.docs_content_list.as_view(),name='docs contents list create'),
    path('create_docs_content/',views.Create_docs_content,name='create docs content'),
    path('get_docs_content/<int:docs_id>/',views.get_details_docs_content,name='docs content detail'),
    path('update_docs_content/<int:docs_id>/',views.update_docs_content,name='update docs content'),
    path('delete_docs_content/<int:docs_id>/',views.delete_docs_content,name='delete docs content'),    
    
    
    ######################################################
    ############# API for Overall course Details ########
    #####################################################

    path('over_all_course_details/',views.get_overall_course_details,name='course details'),

    ##############################################
    ########## API for user activity  ############
    ##############################################
    path('create_activity/',views.create_video_activity,name='create video activity'),
    path('get_activity/<int:activity_id>/',views.get_video_activity_details,name='get video activity'),
    path('update_activity/<int:activity_id>/',views.update_video_activity,name='update video activity'),
    path('delete_activity/<int:activity_id>/',views.delete_video_activity,name='delete video activity'),
    path('activity_list/',views.VideoActivityList.as_view(),name='video activity list'),

    ##############################################
    ########## API FOR SOAR CARD #################
    ###############################################
    
    path('soar_categories/',soar_cattegory_list,name='soar category list create'),
    
    path('soar_categories/<int:pk>/',soar_cattegory_detail,name='soar category detail update delete'),
    
    path('soar_quiz_data/',soar_quiz_data_list,name='soar quiz data list create'),
    
    path('soar_quiz_data/<int:pk>/',soar_quiz_data_detail,name='soar quiz data detail update delete'),
    
    path('soar_quiz_answer/',soar_quiz_answer_list,name='soar quiz answer list create'),
    
    path('create_soar_quiz_answer/',analysis_views.create_quiz_answer_data_calculation,name='create soar quiz answer with calculation'),
    path('soar_quiz_answer/<int:pk>/',soar_quiz_answer_detail,name='soar quiz answer detail update delete'),
    
    path('soar_quiz_average_score/',soar_quiz_Average_score,name='soar quiz average score list create'),
    
    path('soar_quiz_average_score/<int:pk>/',soar_quiz_Average_score_detail,name='soar quiz average score detail update delete'),












































]

