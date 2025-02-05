from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from django.urls import path
from api.views import DailyQuotesView
from users.views_googleAuth import GoogleLoginView
from users.views import RegisterView, login_view, logout_view, upgrade_to_premium, user_info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/daily-quotes/', DailyQuotesView.as_view(), name='daily-quotes'),
    path('api/auth/google/', GoogleLoginView.as_view(), name='google_login'),
    path('api/auth/user_info/',user_info, name='user_info'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/',  logout_view, name='logout'),
    path('upgrade-to-premium/', upgrade_to_premium, name='upgrade-to-premium'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
