from rest_framework.exceptions import APIException


class ProductNotFound(APIException):
    status_code = 404
    default_detail = 'Product with this barcode does not exist'
    default_code = 'product_not_found'


class PaсkagingNotFound(APIException):
    status_code = 402
    default_detail = 'Product don`t pass paсkaging'
    default_code = 'Product_not_found'


class WrongModel(APIException):
    status_code = 402
    default_detail = 'wrong model and barcode'
    default_code = 'wrong_model'


class BarcodeUsed(APIException):
    status_code = 409
    default_detail = 'Product with this barcode is used in enother warehouse do'
    default_code = 'product_used'
