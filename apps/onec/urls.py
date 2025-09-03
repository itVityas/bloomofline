from django.urls import path

from apps.onec.views.weight import Weight1cView
from apps.onec.views.onec_ttn import (
    OneCTTNCreateAPIView,
    OneCTTNListAPIView,
    OneCTTNRetrieveAPIView,
    OneCTTNRetrieveUpdateDestroyAPIView,
    OneCTTNFullCreateAPIView
)
from apps.onec.views.onec_ttn_item import (
    OneCTTNItemCreateListView,
    OneCTTNItemRUDView,
)

urlpatterns = [
    path('1c/weight/', Weight1cView.as_view()),
    path('1c/onec_ttn/create/', OneCTTNCreateAPIView.as_view()),
    path('1c/onec_ttn/full_create/', OneCTTNFullCreateAPIView.as_view()),
    path('1c/onec_ttn/update/<int:pk>/', OneCTTNRetrieveUpdateDestroyAPIView.as_view()),
    path('1c/onec_ttn/detailed/<int:pk>/', OneCTTNRetrieveAPIView.as_view()),
    path('1c/onec_ttn/list/', OneCTTNListAPIView.as_view()),
    path('1c/onec_ttn_item/', OneCTTNItemCreateListView.as_view()),
    path('1c/onec_ttn_item/<int:pk>/', OneCTTNItemRUDView.as_view()),
]
