from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'role', 'username', 'email']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SigninSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=User.ROLE)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        role = data.get('role')
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Utilisateur non trouvé.")

        if user.role != role:
            raise serializers.ValidationError("Rôle incorrect.")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Mot de passe incorrect.")

        return {'user': user}
    

class SignupSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=User.ROLE, default='MANAGER', required=False)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirmation_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['confirmation_password']:
            raise serializers.ValidationError({"password": "Les deux mot de passe ne sont pas identique."})
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Ce nom d'utilisateur est déjà utilisé."})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Cet email est déjà utilisé."})

        return data
    
    def create(self, validated_data):
        validated_data.pop('confirmation_password')

        role = validated_data.get("role", "MANAGER")
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password")

        return User.objects.create_user(
            role=role,
            username=username,
            email=email,
            password=password
        )
    

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Aucun utilisateur trouvé avec cet email.")
        return value


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_old_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError('Ancien mot de passe incorrect.')
        return value
    
    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Le nouveau mot de passe doit contenir au moins 8 caractères.")
        return value
    
    def save(self, **kwargs):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        
        return user
