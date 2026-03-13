from django.urls import path

from apps.woffline.views.warhouse_sync import FullWarehouseSyncView, WarehouseSyncView

urlpatterns = [
    path('full_sync/', FullWarehouseSyncView.as_view()),
    path('sync/', WarehouseSyncView.as_view()),
]
