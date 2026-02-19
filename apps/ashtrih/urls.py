from django.urls import path

from apps.ashtrih.views.model_name import (
    ModelNameListView,
    ModelNameByProductCodeListView,
    ProductCountByModelNameView)
from apps.ashtrih.views.model import ModelListView
from apps.ashtrih.views.product import ProductListView, ProductUpdateClearedView
from apps.ashtrih.views.shtrih_sync import SyncFullStrihView, SyncShtrihView


urlpatterns = [
    path('strih/model_name', ModelNameListView.as_view()),
    path('strih/model_name_by_production_id', ModelNameByProductCodeListView.as_view()),
    path('strih/product_count_by_model_name_id/<int:pk>/', ProductCountByModelNameView.as_view()),
    path('strih/models', ModelListView.as_view()),
    path('strih/products', ProductListView.as_view()),
    path('strih/product_update_cleared/<int:pk>/', ProductUpdateClearedView.as_view()),
    path('strih/sync/', SyncShtrihView.as_view()),
    path('strih/fullsync/', SyncFullStrihView.as_view()),
]
