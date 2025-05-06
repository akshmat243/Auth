from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import SignupSerializer, LoginSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    access  = refresh.access_token
    return Response({
        'access':  str(access),
        'refresh': str(refresh),
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(
        username=serializer.validated_data['username'],
        password=serializer.validated_data['password']
    )
    if not user:
        return Response({'detail': 'Invalid credentials'}, status=401)
    refresh = RefreshToken.for_user(user)
    access  = refresh.access_token
    return Response({
        'access':  str(access),
        'refresh': str(refresh),
    }, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    data = UserSerializer(request.user).data
    return Response(data)


class LogoutAndBlacklistRefreshView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail':'Refresh token required.'}, status=400)
        try:
            RefreshToken(refresh_token).blacklist()
        except:
            return Response({'detail':'Invalid/expired token.'}, status=400)
        return Response({'detail':'Logged out.'}, status=205)