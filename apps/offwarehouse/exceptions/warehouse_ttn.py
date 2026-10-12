from rest_framework.exceptions import APIException


class TTNNotFound(APIException):
    status_code = 404
    default_detail = 'Warehouse TTN not found'
    default_code = 'ttn_not_found'
