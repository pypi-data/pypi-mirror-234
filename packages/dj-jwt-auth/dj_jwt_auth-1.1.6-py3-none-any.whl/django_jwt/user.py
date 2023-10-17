from datetime import datetime
from logging import getLogger

import pytz
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest

from django_jwt import settings
from django_jwt.utils import oidc_handler

utc = pytz.UTC
log = getLogger(__name__)

model = get_user_model()


class UserHandler:
    modified_at = None

    def __init__(self, payload: dict, request: HttpRequest, access_token: str):
        # payload of access token without user info
        # auth0_id should be available if auth0 added in Client Scopes in KeyCloak admin
        self.kwargs = settings.OIDC_USER_DEFAULTS.copy()
        self.kwargs[settings.OIDC_USER_UID] = payload.get("auth0_id", payload["sub"])

        modified_at = payload.get(settings.OIDC_TOKEN_MODIFIED_FIELD, None)
        if modified_at and isinstance(modified_at, int):
            self.modified_at = utc.localize(datetime.fromtimestamp(modified_at))

        self.on_create = settings.OIDC_USER_ON_CREATE
        self.on_update = settings.OIDC_USER_ON_UPDATE
        self.request = request
        self.access_token = access_token

    def _collect_user_data(self):
        """ Collect user data from KeyCloak """

        user_data = oidc_handler.get_user_info(self.access_token)
        self.kwargs["email"] = user_data["email"].lower()
        self.kwargs.update(
            {
                ca_key: user_data[kc_key]
                for kc_key, ca_key in settings.OIDC_USER_MAPPING.items()
                if kc_key in user_data
            }
        )

    def _update_user(self, user):
        """ Update user fields if they are changed """

        is_changed = False
        self._collect_user_data()
        for key, val in self.kwargs.items():
            if getattr(user, key) != val:
                setattr(user, key, val)
                is_changed = True
        if is_changed:
            user.save(update_fields=self.kwargs.keys())

    def _create_new_user(self) -> model:
        """ Create new user if user is not found in database even by email. """

        user = model.objects.create(**self.kwargs)
        if self.on_create:
            self.on_create(user, self.request)
        return user

    def _get_by_email(self) -> model:
        """ Get user from database by email and update to resave kc_id. """

        user = model.objects.get(email=self.kwargs["email"])
        self._update_user(user)
        if self.on_update:
            self.on_update(user, self.request)
        return user

    def _update_existing_user(self, user):
        """ Check modified_at and update user if it is changed in KeyCloak."""

        user_modified_at = getattr(user, settings.OIDC_USER_MODIFIED_FIELD, None)
        if user_modified_at:
            if not user_modified_at.tzinfo:
                user_modified_at = utc.localize(user_modified_at)
            if self.modified_at and user_modified_at < self.modified_at:
                self._update_user(user)
                if self.on_update:
                    self.on_update(user, self.request)

    def get_user(self) -> model:
        """
        Get user from database by kc_id or email.
        If user is not found, create new user.
        Update user fields if they are changed in KeyCloak.
        """

        try:
            user = model.objects.get(**{settings.OIDC_USER_UID: self.kwargs[settings.OIDC_USER_UID]})
            self._update_existing_user(user)
            return user

        except model.DoesNotExist:
            self._collect_user_data()
            try:
                return self._get_by_email()
            except model.DoesNotExist:
                return self._create_new_user()
