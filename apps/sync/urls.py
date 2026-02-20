from django.urls import path

from apps.sync.views.sync import FullSyncAllView, SyncAllView


urlpatterns = [
    path('full_sync/', FullSyncAllView.as_view()),
    path('sync/', SyncAllView.as_view()),
]
