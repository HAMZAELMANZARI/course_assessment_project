from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # Route for the course list / index page
    path('', views.course_list, name='index'),
    path('course/<int:pk>/', views.course_details, name='course_details'),
    path('course/<int:course_id>/enroll/', views.enroll, name='enroll'),

    # Route for the submit view (Task 5)
    path('<int:course_id>/submit/', views.submit, name="submit"),

    # Route for the exam result view (Task 5)
    path('course/<int:course_id>/submission/<int:submission_id>/result/',
         views.show_exam_result, name="exam_result"),

    # Authentication
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]