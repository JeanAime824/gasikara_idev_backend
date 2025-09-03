from django.contrib.auth.decorators  import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

<<<<<<< Updated upstream
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
=======
# Create your views here.
from django.shortcuts import render

from rest_framework.permissions import AllowAny

from .models import CustomUser
from rest_framework import generics, permissions, status
>>>>>>> Stashed changes
from rest_framework.response import Response
from rest_framework.views import APIView

<<<<<<< Updated upstream
from .models import User
from .permissions import IsAdmin, IsResponsableOrHigher
from .serializers import UserSerializer, SigninSerializer, SignupSerializer, PasswordResetSerializer, PasswordChangeSerializer

# Create your views here.
class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            if user.role == 'ADMIN':
                redirect = 'http://localhost:3000/admin'  # URL Frontend React
            else:
                redirect = 'http://localhost:3000/manager'

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
                'redirect': redirect
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]  # SUPERUSER Ou ADMIN seulement peut créer le MANAGER

    def perform_create(self, serializer):
        serializer.save(role='MANAGER')

=======
from rest_framework.generics import GenericAPIView

from django.db.models.functions import TruncMonth
from django.db.models import Count

from .models import CustomUser, Etudiant, Cours, Notification
from .serializers import UserSerializer, SignUpSerializer, SignInSerializer, DashboardSerializer

# Create your views here.
class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Utilisateur crée avec succès'
        }, status=status.HTTP_201_CREATED)
    

class SignInView(GenericAPIView):
    serializer_class = SignInSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        user = validated_data['user']

        return Response({
            'user': UserSerializer(user).data,
            'refresh': validated_data['refresh'],
            'access': validated_data['access'],
            'message': 'Connexion réussie'
        }, status=status.HTTP_200_OK)
    
>>>>>>> Stashed changes

class SignOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Déconnexion réussie"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Token invalide"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Mot de passe modifié avec succès.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.data['email']).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                send_mail(
                    'Reset Password',
                    f'Lien: /reset/{uid}/{token}/',
                    'team.gidev@gmail.com',
                    [user.email]
                )
            return Response({'message': 'Le lien d\'instruction d\'initialisation de mot de passe à été envoyé par Email.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')

        if not password:
            return Response({'error': 'Mot de passe requis'}, status=400)
        
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Lien invalide'}, status=400)
        
        if default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            
<<<<<<< Updated upstream
            return Response({'message': 'Mot de passe réinitialisé avec succès'})
        
        return Response({'error': 'Token invalide'}, status=400)
=======
        except TokenError:
            return Response(
                {'error': 'Refresh token invalide'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
class DashboardView(APIView):
    permission_classes = [AllowAny]
    # Récupération des données sur le dashboard
    def get(self, request, *args, **kwargs):
        nombre_etudiant = Etudiant.objects.count()
        nombre_cours = Cours.objects.count()

        tendance_inscription = Etudiant.objects.annotate(
            mois_inscription = TruncMonth('date_inscription')
        ).values('mois_inscription').annotate(
            nombre_etudiant = Count('id')
        ).order_by('mois_inscription')

        tendance_inscription_dict = {
            item['mois_inscription'].strftime('%Y-%m'): item['nombre_etudiant']
            for item in tendance_inscription
        }

        repartition_filiere = Etudiant.objects.values(
            'filiere__nom'
        ).annotate(
            nombre_etudiant = Count('id')
        ).order_by('-nombre_etudiant')

        repartition_filiere_dict = {
            item['filiere__nom'] if item['filiere__nom'] else 'Non assigné': item['nombre_etudiant']
            for item in repartition_filiere
        }

        notification_recent = Notification.objects.filter(
            est_lue = False
        ).order_by('-date_creation')[:5]

        dashboard_data = {
            'nombre_etudiant': nombre_etudiant,
            'nombre_cours': nombre_cours,
            'tendance_inscription': tendance_inscription_dict,
            'repartition_filiere': repartition_filiere_dict,
            'notification_recent': notification_recent,
        }

        serializer = DashboardSerializer(dashboard_data)

        return Response(serializer.data)
>>>>>>> Stashed changes
