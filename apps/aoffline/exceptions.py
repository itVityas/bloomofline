from rest_framework.exceptions import ValidationError


class OldPasswordException(ValidationError):
    default_detail = 'Wrong old password'


class PasswordException(ValidationError):
    default_detail = 'passwords do not match'


class PasswordEmptyException(ValidationError):
    default_detail = 'password can`t be empty'


class UserNotFountException(ValidationError):
    default_detail = 'Username and password do not match'


class EmptyUserException(ValidationError):
    default_detail = 'Username can`t be empty'
