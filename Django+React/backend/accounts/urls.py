from django.urls import path
from .views import signup_view, login_view, LogoutAndBlacklistRefreshView, dashboard_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('logout/', LogoutAndBlacklistRefreshView.as_view(), name='token_logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    
]