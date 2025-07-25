from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from drf_spectacular.utils import extend_schema

from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSignupSerializer, UserSigninSerializer, MyTokenObtainPairSerializer, UserProfileSerializer, \
    ChangePasswordSerializer, ReactivateAccountSerializer, PasswordResetRequestSerializer, \
    PasswordResetConfirmSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

User = get_user_model()

@extend_schema(
    summary="User Signup",
    request=UserSignupSerializer,
    responses={201: {'description': 'User created successfully.'}}
)
class SignupView(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({"message": "Signup endpoint. Please POST your data."})


class SigninView(APIView):

    @extend_schema(
        summary="User Login",
        request=UserSigninSerializer,
        responses={200: {'description': 'Returns access and refresh tokens.'}}
    )

    def post(self, request):
        serializer = UserSigninSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                user.last_login = timezone.now()
                user.save()  # Save the updated last_login
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View for the currently authenticated user to retrieve and update their profile.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Returns the user object for the currently authenticated user
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            tokens = OutstandingToken.objects.filter(user_id=self.object.id)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            return Response({"status": "password set successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeactivateAccountView(APIView):
    """
    View to deactivate the user's account.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Deactivate User Account", request=None,
                   responses={200: {'description': 'Account deactivated successfully'}})
    def post(self, request, *args, **kwargs):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"status": "Account deactivated successfully"}, status=status.HTTP_200_OK)


class ReactivateAccountView(APIView):
    """
    View to reactivate a user's account by providing their credentials.
    Does not require authentication.
    """
    permission_classes = [AllowAny]  # Anyone can attempt to reactivate

    @extend_schema(summary="Reactivate User Account", request=ReactivateAccountSerializer,
                   responses={200: {'description': 'Account reactivated successfully'}})
    def post(self, request, *args, **kwargs):
        serializer = ReactivateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        # If validation passed, the user is authenticated and inactive.
        # Now, we reactivate them.
        user.is_active = True
        user.save()

        return Response({"status": "Account reactivated successfully. You can now log in."}, status=status.HTTP_200_OK)


class DeleteAccountView(APIView):
    """
    View to permanently delete the user's account.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Delete User Account Permanently", request=None,
                   responses={204: {'description': 'Account deleted permanently'}})
    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"status": "Account deleted permanently"}, status=status.HTTP_204_NO_CONTENT)


class PasswordResetRequestView(generics.GenericAPIView):
    """
    View to request a password reset.
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        # Generate token and UID
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        # Construct reset link (customize the domain for your frontend)
        reset_link = f"http://localhost:3000/reset-password?uidb64={uidb64}&token={token}"

        # Send email
        send_mail(
            'Password Reset Request',
            f'Hi {user.username},\n\nPlease use the following link to reset your password:\n{reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response({"status": "Password reset link sent to your email."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    View to confirm and set a new password.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        new_password = serializer.validated_data['new_password']

        user.set_password(new_password)
        user.save()

        tokens = OutstandingToken.objects.filter(user_id=user.id)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        return Response({"status": "Password has been reset successfully."}, status=status.HTTP_200_OK)
