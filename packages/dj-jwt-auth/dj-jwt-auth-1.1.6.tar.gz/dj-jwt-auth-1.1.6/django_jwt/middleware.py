from http import HTTPStatus
from logging import getLogger

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from jwt import ExpiredSignatureError

from django_jwt.user import UserHandler
from django_jwt.utils import oidc_handler

log = getLogger(__name__)


class JWTAuthMiddleware(MiddlewareMixin):
    header_key = "HTTP_AUTHORIZATION"

    def process_request(self, request):
        if self.header_key not in request.META:
            return

        auth_header = request.META[self.header_key]
        if not auth_header.startswith("Bearer "):
            return

        # auth part
        raw_token = auth_header[7:]
        try:
            info = oidc_handler.decode_token(raw_token)
            request.user = request._cached_user = UserHandler(info, request, raw_token).get_user()
        except ExpiredSignatureError:
            return JsonResponse(status=HTTPStatus.UNAUTHORIZED.value, data={"detail": "expired token"})
        except UnicodeDecodeError as exc:
            log.warning(f"UnicodeDecodeError: {exc}")
        except Exception as exc:
            log.warning(f"Unexpected error: {exc}")
            return
