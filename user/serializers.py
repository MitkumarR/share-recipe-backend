from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class UserSigninSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['role'] = user.role
        token['email'] = user.email
        token['username'] = user.username

        return token

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and updating the user's own profile.
    """
    class Meta:
        model = User
        fields = ('email', 'username', 'bio', 'profile_picture', 'role', 'date_joined')
        read_only_fields = ('email', 'role','date_joined') # These fields should not be editable here

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        # Here you can add custom password validation logic if needed
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value


class ReactivateAccountSerializer(serializers.Serializer):
    """
    Serializer for the account reactivation endpoint.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials.")

        # Now, check if the account is already active
        if user.is_active:
            raise serializers.ValidationError("This account is already active.")

        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset.
    """
    new_password = serializers.CharField(write_only=True, required=True)
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            uid = smart_str(urlsafe_base64_decode(attrs['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('Invalid token or user ID.')

        if not PasswordResetTokenGenerator().check_token(user, attrs['token']):
            raise serializers.ValidationError('Invalid token or user ID.')

        attrs['user'] = user
        return attrs