from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from zippy_form.models import Account
from .utils import ACCOUNT_STATUS
from rest_framework import status


class IsAccountActive(BasePermission):
    """
    Permission To Check If Account Is Active
    """
    def has_permission(self, request, view):
        if 'ZF-SECRET-KEY' not in request.headers:
            raise AuthenticationFailed({"status": "permission_error", "detail": "Secret Key Required."},
                                       status.HTTP_401_UNAUTHORIZED)

        account_id = request.headers['ZF-SECRET-KEY']
        try:
            account = Account.objects.filter(id=account_id).first()

            if account is None:
                raise AuthenticationFailed({"status": "permission_error", "detail": "Invalid Secret Key."},
                                           status.HTTP_401_UNAUTHORIZED)
            elif account.status != ACCOUNT_STATUS[1][0]:
                raise AuthenticationFailed({"status": "permission_error", "detail": "Account Not Active."},
                                           status.HTTP_401_UNAUTHORIZED)
            else:
                return True
        except Exception as e:
            raise AuthenticationFailed({"status": "permission_error", "detail": "Invalid Secret Key."},
                                       status.HTTP_401_UNAUTHORIZED)

