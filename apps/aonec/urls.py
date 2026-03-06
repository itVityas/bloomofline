from django.urls import path

from apps.aonec.views.onec_ttn import (
    OfflineOneCTTNListAPIView,
    OfflineOneCTTNRetrieveAPIView,
)
from apps.aonec.views.onec_ttn_item import (
    OfflineOneCTTNItemListView,
)
from apps.aonec.views.onec_sync import SyncFullOneCView, SyncOneCView

urlpatterns = [
    path('1c/onec_ttn/detailed/<int:pk>/', OfflineOneCTTNRetrieveAPIView.as_view()),
    path('1c/onec_ttn/list/', OfflineOneCTTNListAPIView.as_view()),
    path('1c/onec_ttn_item/', OfflineOneCTTNItemListView.as_view()),
    path('1c/sync/', SyncOneCView.as_view()),
    path('1c/fullsync/', SyncFullOneCView.as_view()),
]
