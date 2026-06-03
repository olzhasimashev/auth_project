from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import User, AccessRule
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, AccessRuleSerializer
from .permissions import CustomRABACPermission, IsAdminRole


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Успешный выход из системы."}, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class SoftDeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        user.auth_token.delete()  
        return Response({"detail": "Аккаунт успешно деактивирован (мягкое удаление)."}, status=status.HTTP_200_OK)



class AccessRuleViewSet(viewsets.ModelViewSet):
    
    queryset = AccessRule.objects.all()
    serializer_class = AccessRuleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminRole]



class MockInvoiceListView(APIView):
    
    permission_classes = [IsAdminRole | CustomRABACPermission]
    resource_name = 'invoice' 

    def get(self, request):
        mock_data = [
            {"id": 1, "amount": 50000, "currency": "KZT", "status": "Paid"},
            {"id": 2, "amount": 120000, "currency": "KZT", "status": "Pending"}
        ]
        return Response(mock_data, status=status.HTTP_200_OK)

    def post(self, request):
        return Response({"detail": "Счет успешно создан (Mock)."}, status=status.HTTP_201_CREATED)

class MockAnalyticsView(APIView):
    
    permission_classes = [IsAdminRole | CustomRABACPermission]
    resource_name = 'analytics'

    def get(self, request):
        mock_analytics = {"views": 1500, "conversions": 3.4, "period": "May 2026"}
        return Response(mock_analytics, status=status.HTTP_200_OK)