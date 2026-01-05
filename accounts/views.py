from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.core.mail import send_mail

# ------------ Login/Signup Section -----------------------
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


# Signup
@api_view(["POST"])
def signup(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response(
            {"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
        )
    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, email=email, password=password)

    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "message": "Account created successfully",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        },
        status=status.HTTP_201_CREATED,
    )


# Login
@api_view(["POST"])
def login_user(request):
    identifier = request.data.get("email_or_username")
    password = request.data.get("password")

    if not identifier or not password:
        return Response(
            {"error": "Email/Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        if "@" in identifier:
            user_obj = User.objects.get(email=identifier)
        else:
            user_obj = User.objects.get(username=identifier)
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

    user = authenticate(username=user_obj.username, password=password)

    if not user:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        },
        status=status.HTTP_200_OK,
    )


# User Profile Page
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response(
        {
            "username": request.user.username,
            "email": request.user.email,
        }
    )


# Updating profile details email and password
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    email = request.data.get("email")
    username = request.data.get("username")

    if not email and not username:
        return Response(
            {"error": "Provide at least one field to update."}, status=status.HTTP_400_BAD_REQUEST
        )
    #Checking if email or username are already taken
    if email:
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            return Response(
                {"error": "Email is already taken"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.email = email
    
    if username:    
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            return Response(
                {"error": "Username is already taken"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.username = username
        
    user.save()
    return Response({"message": "Profile updated"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")

    if not old_password or not new_password:
        return Response(
            {"error": "Old password and new password required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not user.check_password(old_password):
        return Response(
            {"error": "Old password incorrect"}, status=status.HTTP_400_BAD_REQUEST
        )

    user.set_password(new_password)
    user.save()

    return Response({"message": "Password changed successfully"})

#Sending Emails through Support Page
@api_view(["POST"])
def support_request(request):
    name = request.data.get("name")
    email = request.data.get("email")
    message = request.data.get("message")
    
    if not name or not email or not message:
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST
        )
        
    try:
        send_mail(
            subject=f"Support Request from {name}",
            message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            from_email=email,
            recipient_list=['jianpantoronto@gmail.com'],
        )
        return Response({"message": "Support request sent successfully!"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

