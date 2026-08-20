from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer


@extend_schema(tags=['Authentication'])
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({
            'success': False,
            'errors': {'detail': 'Username and password are required.'},
        }, status=400)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({
            'success': False,
            'errors': {'detail': 'Invalid credentials.'},
        }, status=401)

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    access['token_type'] = 'access'
    access['username'] = user.username

    return Response({
        'success': True,
        'data': {
            'access_token': str(access),
            'refresh_token': str(refresh),
            'user': UserSerializer(user).data,
        },
        'message': 'Login successful.',
    })


@extend_schema(tags=['Authentication'])
@api_view(['GET'])
@permission_classes([AllowAny])
def verify_token(request):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return Response({
            'success': False,
            'errors': {'detail': 'Authorization header must start with Bearer.'},
        }, status=401)

    token = auth_header.split(' ', 1)[1]
    try:
        from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
        from rest_framework_simplejwt.views import TokenRefreshView
        token_obj = RefreshToken(token)
        token_obj.verify()

        return Response({
            'success': True,
            'data': {
                'valid': True,
                'username': token_obj['username'],
            },
            'message': 'Token is valid.',
        })
    except (InvalidToken, TokenError) as e:
        return Response({
            'success': False,
            'errors': {'detail': str(e)},
        }, status=401)