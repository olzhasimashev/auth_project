from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from .models import UserRole, AccessRule, Resource, Action

class CustomRABACPermission(BasePermission):
    """
    Проверяет доступ пользователя на основе запрашиваемого Ресурса и Действия.
    Каждая View, защищенная этим классом, должна объявить `resource_name`.
    """
    
    def has_permission(self, request, view):
        # 1. Проверка аутентификации (401 Error)
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated()
            
        if not request.user.is_active:
            raise NotAuthenticated(detail="Учетная запись деактивирована.")

        # Получаем имя ресурса из View
        resource_name = getattr(view, 'resource_name', None)
        if not resource_name:
            return True # Если ресурс не указан, пропускаем (или закрываем по дефолту)

        # Маппинг HTTP методов на кастомные Actions
        method_map = {
            'GET': 'read',
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete'
        }
        action_name = method_map.get(request.method)

        # Получаем роли пользователя
        user_roles = UserRole.objects.filter(user=request.user).values_list('role_id', flat=True)
        if not user_roles:
            raise PermissionDenied() # 403 Error

        # Проверяем наличие разрешающего правила в БД
        has_access = AccessRule.objects.filter(
            role_id__in=user_roles,
            resource__name=resource_name,
            action__name=action_name,
            is_allowed=True
        ).exists()

        if not has_access:
            raise PermissionDenied() # 403 Error

        return True

class IsAdminRole(BasePermission):
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated()
        
        return request.user.user_roles.filter(role__name='Admin').exists()