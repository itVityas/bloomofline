from django.urls import path

from apps.aonec.views.onec_ttn import (
    OfflineOneCTTNCreateAPIView,
    OfflineOneCTTNListAPIView,
    OfflineOneCTTNRetrieveAPIView,
    OfflineOneCTTNRetrieveUpdateDestroyAPIView,
    OfflineOneCTTNFullCreateAPIView
)
from apps.aonec.views.onec_ttn_item import (
    OfflineOneCTTNItemCreateListView,
    OfflineOneCTTNItemRUDView,
)
from apps.aonec.views.onec_sync import SyncFullOneCView, SyncOneCView

urlpatterns = [
    path('1c/onec_ttn/create/', OfflineOneCTTNCreateAPIView.as_view()),
    path('1c/onec_ttn/full_create/', OfflineOneCTTNFullCreateAPIView.as_view()),
    path('1c/onec_ttn/update/<int:pk>/', OfflineOneCTTNRetrieveUpdateDestroyAPIView.as_view()),
    path('1c/onec_ttn/detailed/<int:pk>/', OfflineOneCTTNRetrieveAPIView.as_view()),
    path('1c/onec_ttn/list/', OfflineOneCTTNListAPIView.as_view()),
    path('1c/onec_ttn_item/', OfflineOneCTTNItemCreateListView.as_view()),
    path('1c/onec_ttn_item/<int:pk>/', OfflineOneCTTNItemRUDView.as_view()),
    path('1c/sync/', SyncOneCView.as_view()),
    path('1c/fullsync/', SyncFullOneCView.as_view()),
]
