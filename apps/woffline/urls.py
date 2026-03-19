from django.urls import path

from apps.woffline.views.warhouse_sync import FullWarehouseSyncView, WarehouseSyncView
from apps.woffline.views.type_of_work import OfflineTypeOfWorkListView
from apps.woffline.views.warehouse_action import OfflineWarehouseActionListView, OfflineWarehouseActionRetrieveView
from apps.woffline.views.warehouse import OfflineWarehouseListView

urlpatterns = [
    path('full_sync/', FullWarehouseSyncView.as_view()),
    path('sync/', WarehouseSyncView.as_view()),
    path('warehouse/typeofwork/', OfflineTypeOfWorkListView.as_view()),
    path('warehouse/action/', OfflineWarehouseActionListView.as_view()),
    path('warehouse/action/<int:pk>/', OfflineWarehouseActionRetrieveView.as_view()),
    path('warehouse/warehouse/', OfflineWarehouseListView.as_view()),
]
