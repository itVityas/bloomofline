from django.urls import path

from apps.ashtrih.views.model_name import (
    OfflineModelNameListView,
    OfflineModelNameByProductCodeListView,
    OfflineProductCountByModelNameView)
from apps.ashtrih.views.model import OfflineModelListView
from apps.ashtrih.views.product import OfflineProductListView
from apps.ashtrih.views.shtrih_sync import SyncFullStrihView, SyncShtrihView


urlpatterns = [
    path('strih/model_name', OfflineModelNameListView.as_view()),
    path('strih/model_name_by_production_id', OfflineModelNameByProductCodeListView.as_view()),
    path('strih/product_count_by_model_name_id/<int:pk>/', OfflineProductCountByModelNameView.as_view()),
    path('strih/models', OfflineModelListView.as_view()),
    path('strih/products', OfflineProductListView.as_view()),
    path('strih/sync/', SyncShtrihView.as_view()),
    path('strih/fullsync/', SyncFullStrihView.as_view()),
]
