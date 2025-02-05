from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Remove password2 from the validated_data as it's not needed for user creation
        validated_data.pop('password2', None)
        
        # Create user instance but don't save it yet
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_active=True
        )
        
        # Set the password properly (this will hash the password)
        user.set_password(validated_data['password'])
        
        # Initialize premium attributes if they exist in your user model
        if hasattr(user, 'is_premium'):
            user.is_premium = False
        if hasattr(user, 'premium_start_date'):
            user.premium_start_date = None
        if hasattr(user, 'premium_end_date'):
            user.premium_end_date = None
            
        # Save the user instance
        user.save()
        
        return user

    def to_representation(self, instance):
        # Control what data is returned after registration
        data = super().to_representation(instance)
        data.pop('password', None)  # Remove password from response
        data.pop('password2', None)  # Remove password2 from response
        
        # Add additional user info if needed
        if hasattr(instance, 'is_premium'):
            data['is_premium'] = instance.is_premium
        
        return data
