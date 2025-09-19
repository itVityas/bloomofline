from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.aoffline.views.role import RoleListCreateView, RoleDetailedView
from apps.aoffline.views.user_roles import (
    UserRolesListView, UserRolesDetailedView)
from apps.aoffline.views.user import (
    UserListView, UserDetailedView, UserRetrieveView, UserRoleDeleteView)
from apps.aoffline.views.register import RegistrationView
from apps.aoffline.views.change_password import ChangePasswordView, ChangeUserPasswordView
from apps.aoffline.serializers.autorization import CustomTokenObtainPairSerializer
from apps.aoffline.views.sync import SyncAccountView

urlpatterns = [
    # user
    path('login/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer)),
    path('change_password/', ChangePasswordView.as_view()),
    path('change_user_password/', ChangeUserPasswordView.as_view(), name='change_user_password'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailedView.as_view(), name='user-update'),
    path('user/detailed/<int:pk>/', UserRetrieveView.as_view(), name='user-detail'),
    path('user/roledelete/', UserRoleDeleteView.as_view(), name='userroledelete'),
    # user role
    path('role/', RoleListCreateView.as_view(), name='listcreate-role'),
    path('role/<int:pk>/', RoleDetailedView.as_view(), name='update-role'),
    path('userroles/', UserRolesListView.as_view(), name='userrole-list'),
    path('userroles/<int:pk>/', UserRolesDetailedView.as_view(), name='userrole-detailed'),
    # sync
    path('sync/', SyncAccountView.as_view(), name='account_sync')
]
