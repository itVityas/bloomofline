from django.urls import path

from apps.warehouse.views.type_of_work import (
    TypeOfWorkListCreateView,
    TypeOfWorkRetrieveUpdateDestroyView
)
from apps.warehouse.views.warehouse import (
    WarehouseListCreateView,
    WarehouseRetrieveUpdateDestroyView
)
from apps.warehouse.views.warehouse_action import (
    WarehouseActionCreateView,
    WarehouseActionListView,
    WarehouseActionRetrieveUpdateDestroyView,
    WarehouseActionRetrieveView
)
from apps.warehouse.views.pallet import (
    PalletListCreateAPIView,
    PalletRetrieveUpdateDestroyView,
    PalletCreateByTTNAPIView
)
from apps.warehouse.views.warehouse_ttn import (
    WarehouseTTNCreateAPIView,
    WarehouseTTNListAPIView,
    WarehouseTTNRetrieveUpdateDestroyAPIView,
    WarehouseTTNRetrieveAPIView,
    WarehouseTTNByUserIdAPIView,
    WarehouseTTNProductsAPIView,
    WarehouseTTNProductsByUserIdAPIView,
)
from apps.warehouse.views.warehouse_do import (
    WarehouseDoListAPIView,
    WarehouseDoRetrieveUpdateDestroyAPIView,
    WarehouseDoRetrieveAPIView,
)

urlpatterns = [
    path('typeofwork/', TypeOfWorkListCreateView.as_view()),
    path('typeofwork/<int:pk>/', TypeOfWorkRetrieveUpdateDestroyView.as_view()),
    path('warehouse/', WarehouseListCreateView.as_view()),
    path('warehouse/<int:pk>/', WarehouseRetrieveUpdateDestroyView.as_view()),
    path('warehouseaction/create/', WarehouseActionCreateView.as_view()),
    path('warehouseaction/update/<int:pk>/', WarehouseActionRetrieveUpdateDestroyView.as_view()),
    path('warehouseaction/list/', WarehouseActionListView.as_view()),
    path('warehouseaction/detailed/<int:pk>/', WarehouseActionRetrieveView.as_view()),
    path('pallet/', PalletListCreateAPIView.as_view()),
    path('pallet/<int:pk>/', PalletRetrieveUpdateDestroyView.as_view()),
    path('pallet/create_by_ttn/', PalletCreateByTTNAPIView.as_view()),
    path('warehousettn/create/', WarehouseTTNCreateAPIView.as_view()),
    path('warehousettn/list/', WarehouseTTNListAPIView.as_view()),
    path('warehousettn/detailed/<str:ttn_number>/', WarehouseTTNRetrieveAPIView.as_view()),
    path('warehousettn/update/<str:ttn_number>/', WarehouseTTNRetrieveUpdateDestroyAPIView.as_view()),
    path('warehousettn/user/', WarehouseTTNByUserIdAPIView.as_view()),
    path('warehousettn/products/<str:ttn_number>/', WarehouseTTNProductsAPIView.as_view()),
    path('warehousettn/productsuser/', WarehouseTTNProductsByUserIdAPIView.as_view()),
    path('warehouse_do/list/', WarehouseDoListAPIView.as_view()),
    path('warehouse_do/detailed/<int:pk>/', WarehouseDoRetrieveAPIView.as_view()),
    path('warehouse_do/update/<int:pk>/', WarehouseDoRetrieveUpdateDestroyAPIView.as_view()),
]
