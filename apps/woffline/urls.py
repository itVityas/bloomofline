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
from apps.woffline.views.warehouse_ttn import (
    OfflineWarehouseTTNByUserIdAPIView,
    OfflineWarehouseTTNCreateAPIView,
    OfflineWarehouseTTNListAPIView,
    OfflineWarehouseTTNProductsAPIView,
    OfflineWarehouseTTNRetrieveAPIView,
    OfflineWarehouseTTNProductsByUserIdAPIView,
    OfflineWarehouseTTNRetrieveUpdateDestroyAPIView,
)
from apps.woffline.views.warehouse_do import (
    OfflineWarehouseDoBarcodePalletAPIView,
    OfflineWarehouseDoCreateAPIView,
    OfflineWarehouseDoListAPIView,
    OfflineWarehouseDoRetrieveAPIView,
    OfflineWarehouseDoRetrieveUpdateDestroyAPIView
)
from apps.woffline.views.shipment import (
    OfflineShipmentBarcodeRetrieveAPIView,
    OfflineShipmentCreateAPIView,
    OfflineShipmentRetrieveAPIView,
    OfflineShipmentRetrieveUpdateDestroyAPIView,
    OfflineShipmentListAPIView
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
    path('warehouse/ttn/', OfflineWarehouseTTNListAPIView.as_view()),
    path('warehouse/ttn/create/', OfflineWarehouseTTNCreateAPIView.as_view()),
    path('warehouse/ttns/<str:ttn_number>/', OfflineWarehouseTTNRetrieveAPIView.as_view()),
    path('warehouse/ttn/update/<str:ttn_number>/', OfflineWarehouseTTNRetrieveUpdateDestroyAPIView.as_view()),
    path('warehouse/ttn/user/', OfflineWarehouseTTNByUserIdAPIView.as_view()),
    path('warehouse/ttn/products/<str:ttn_number>/', OfflineWarehouseTTNProductsAPIView.as_view()),
    path('warehouse/ttn/product/user/', OfflineWarehouseTTNProductsByUserIdAPIView.as_view()),
    path('warehouse/do/', OfflineWarehouseDoListAPIView.as_view()),
    path('warehouse/do/create/', OfflineWarehouseDoCreateAPIView.as_view()),
    path('warehouse/do/retrieve/<int:pk>/', OfflineWarehouseDoRetrieveAPIView.as_view()),
    path('warehouse/do/update/<int:pk>/', OfflineWarehouseDoRetrieveUpdateDestroyAPIView.as_view()),
    path('warehouse/do/barcode/', OfflineWarehouseDoBarcodePalletAPIView.as_view()),
    path('shipment/create/', OfflineShipmentCreateAPIView.as_view()),
    path('shipment/', OfflineShipmentListAPIView.as_view()),
    path('shipment/retrieve/<int:pk>/', OfflineShipmentRetrieveAPIView.as_view()),
    path('shipment/update/<int:pk>/', OfflineShipmentRetrieveUpdateDestroyAPIView.as_view()),
    path('shipment/barcode/', OfflineShipmentBarcodeRetrieveAPIView.as_view()),
]
