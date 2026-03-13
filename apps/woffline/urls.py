from django.urls import path

from apps.woffline.views.warhouse_sync import FullWarehouseSyncView

urlpatterns = [
    path('full_sync/', FullWarehouseSyncView.as_view()),
]
