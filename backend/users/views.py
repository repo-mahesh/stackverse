from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import PremiumUser
from users.serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import generics

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    print(user)
    return Response({
        'id': user.id,
        "email": user.email,
        "name": user.name,
        "is_premium": user.is_premium,
        "picture": user.profile_picture,
        "first_name": user.first_name,
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upgrade_to_premium(request):
    user = request.user
    duration = request.data.get('duration', 30)  # Get duration from request or use default
    
    try:
        user.activate_premium(duration_days=duration)
        return Response({
            'status': 'success',
            'message': 'Premium activated successfully',
            'premium_end_date': user.premium_end_date
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=400)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def cancel_premium(request):
#     user = request.user
#     user.deactivate_premium()
#     return Response({
#         'status': 'success',
#         'message': 'Premium deactivated'
#     })

# View to check premium status
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_premium_status(request):
    user = request.user
    return Response({
        'is_premium_active': user.is_premium_active,
        'premium_end_date': user.premium_end_date,
        'premium_start_date': user.premium_start_date
    })




class RegisterView(generics.CreateAPIView):
    queryset = PremiumUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for automatic login
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "status": "success",
            "message": "User created successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_premium_active": user.is_premium_active,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'status': 'fail',
            'message': 'Please provide both username and password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'status': 'success',
            'message': 'Login successful',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_premium_active': user.is_premium_active,
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'status': 'fail',
            'message': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'status': 'success',
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'message': 'Refresh token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'status': 'error',
            'message': 'Invalid token'
        }, status=status.HTTP_400_BAD_REQUEST)

