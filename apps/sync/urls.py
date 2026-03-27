from django.urls import path

from apps.sync.views.sync import FullSyncAllView, SyncAllView
from apps.sync.views.global_state import GlobalStateView, GlobalStateSetFalseView, CheckGlobalStateView


urlpatterns = [
    path('full_sync/', FullSyncAllView.as_view()),
    path('sync/', SyncAllView.as_view()),
    path('mssqlstate/', GlobalStateView.as_view()),
    path('mssqlstatefalse/', GlobalStateSetFalseView.as_view()),
    path('mssqlstatecheck/', CheckGlobalStateView.as_view()),
]
