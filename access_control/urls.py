from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, LogoutView, ProfileView, SoftDeleteUserView,
    AccessRuleViewSet, MockInvoiceListView, MockAnalyticsView
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'rules', AccessRuleViewSet, basename='accessrule')

urlpatterns = [
    # Auth & Profile
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/profile/delete/', SoftDeleteUserView.as_view(), name='profile-delete'),
    
    # Admin System
    path('admin/', include(router.urls)),
    
    # Mock Business Objects
    path('business/invoices/', MockInvoiceListView.as_view(), name='mock-invoices'),
    path('business/analytics/', MockAnalyticsView.as_view(), name='mock-analytics'),

    #Rules
    path('', include(router.urls)),
]