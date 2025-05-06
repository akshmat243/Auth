from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('send-otp/', send_otp, name='send_otp'),
    #path('verify-otp/', verify_otp_view, name='verify_otp'),
    
    path('verify-email/<int:user_id>/', verify_email, name='verify_email'),
    path('verify-mobile/<str:username>/', verify_mobile, name='verify_mobile'),
]