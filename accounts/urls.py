from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "accounts"

urlpatterns = [
    #JWT Authentication Routes
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    #Custom Views
    path("login/", views.login_user, name="login"),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
    path("update-profile/", views.update_profile, name="update_profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("support-request/", views.support_request, name="support_request"),
]