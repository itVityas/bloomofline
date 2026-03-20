from django.urls import path

from apps.woffline.views.warhouse_sync import FullWarehouseSyncView, WarehouseSyncView
from apps.woffline.views.type_of_work import OfflineTypeOfWorkListView
from apps.woffline.views.warehouse_action import OfflineWarehouseActionListView, OfflineWarehouseActionRetrieveView
from apps.woffline.views.warehouse import OfflineWarehouseListView
from apps.woffline.views.pallet import (
    OfflinePalletCreateByTTNAPIView,
    OfflinePalletListCreateAPIView,
    OfflinePalletRetrieveUpdateDestroyView)
from apps.woffline.views.warehouse_products import (
    OfflineWarehouseProductCreateAPIView,
    OfflineWarehouseProductCreateByBarcodeAPIView,
    OfflineWarehouseProductRetrieveAPIView,
    OfflineWarehouseProductListAPIView,
    OfflineWarehouseProductRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('full_sync/', FullWarehouseSyncView.as_view()),
    path('sync/', WarehouseSyncView.as_view()),
    path('warehouse/typeofwork/', OfflineTypeOfWorkListView.as_view()),
    path('warehouse/action/', OfflineWarehouseActionListView.as_view()),
    path('warehouse/action/<int:pk>/', OfflineWarehouseActionRetrieveView.as_view()),
    path('warehouse/warehouse/', OfflineWarehouseListView.as_view()),
    path('warehouse/pallet/', OfflinePalletListCreateAPIView.as_view()),
    path('warehouse/pallet/<int:pk>/', OfflinePalletRetrieveUpdateDestroyView.as_view()),
    path('warehouse/pallet/generate/', OfflinePalletCreateByTTNAPIView.as_view()),
    path('warehouse/product/', OfflineWarehouseProductListAPIView.as_view()),
    path('warehouse/product/<int:pk>/', OfflineWarehouseProductRetrieveAPIView.as_view()),
    path('warehouse/product/create/', OfflineWarehouseProductCreateAPIView.as_view()),
    path('warehouse/product/create/barcode/', OfflineWarehouseProductCreateByBarcodeAPIView.as_view()),
    path('warehouse/product/updaet/<int:pk>/', OfflineWarehouseProductRetrieveUpdateDestroyView.as_view()),
]
