from django.urls import path

from apps.shtrih.views.barcode_full_info import BarcodeFullInfoView

urlpatterns = [
    path('barcode/online/full_info/', BarcodeFullInfoView.as_view()),
]
