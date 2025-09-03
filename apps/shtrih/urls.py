from django.urls import path

from apps.shtrih.views.color import ColorsListView, ColorsByModelNameListView
from apps.shtrih.views.module import ModulesListView
from apps.shtrih.views.production_code import ProductionCodeListView
from apps.shtrih.views.model_name import (
    ModelNameListView,
    ModelNameByProductCodeListView,
    ProductCountByModelNameView)
from apps.shtrih.views.model import ModelListView
from apps.shtrih.views.product import ProductListView
from apps.shtrih.views.barcode_date import DateFromBarcodeView

urlpatterns = [
    path('strih/colors', ColorsListView.as_view()),
    path('strih/colors_by_model_name', ColorsByModelNameListView.as_view()),
    path('strih/modules', ModulesListView.as_view()),
    path('strih/production_code', ProductionCodeListView.as_view()),
    path('strih/model_name', ModelNameListView.as_view()),
    path('strih/model_name_by_production_id', ModelNameByProductCodeListView.as_view()),
    path('strih/product_count_by_model_name_id/<int:pk>/', ProductCountByModelNameView.as_view()),
    path('strih/models', ModelListView.as_view()),
    path('strih/products', ProductListView.as_view()),
    path('strih/barcode_date/', DateFromBarcodeView.as_view()),
]
