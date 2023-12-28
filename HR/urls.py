from django.urls import path
from . import views


app_name = 'HR'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),  # Fixed the missing slash
    path('employee_profile/', views.employee_profile, name='employee_profile'),
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employee_complaints/', views.employee_complaints, name='employee_complaints'),
    path('employee_feedback/', views.employee_feedback, name='employee_feedback'),
    path('complaints/', views.complaints, name='complaints'),
    path('feedback/', views.feedback, name='feedback'),
    path('about/', views.about, name='about'),
]
