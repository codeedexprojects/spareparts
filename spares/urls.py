from django.urls import path
from spares import views


urlpatterns = [
    
    path('register/', views.register, name='user-register'),
    path('verify-otp/', views.verify, name='verify'),
    path('login/',views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view(), name='logout'),



]