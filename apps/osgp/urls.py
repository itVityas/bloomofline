from django.urls import path

from apps.osgp.views.sgp_sync import SyncFullSGPView, SyncSGPView


urlpatterns = [
    path('sgp/full_sync/', SyncFullSGPView.as_view()),
    path('sgp/sync/', SyncSGPView.as_view()),
]
