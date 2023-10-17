from django.conf import settings

OIDC_AUDIENCE = getattr(settings, "OIDC_AUDIENCE", ["account", "broker"])
OIDC_CONFIG_URL = getattr(settings, "OIDC_CONFIG_URL", None)

# key from KeyCloak; value is user model
OIDC_USER_UPDATE = getattr(settings, "OIDC_USER_UPDATE", True)
OIDC_USER_MODIFIED_FIELD = getattr(settings, "OIDC_USER_MODIFIED_FIELD", "modified_timestamp")
OIDC_TOKEN_MODIFIED_FIELD = getattr(settings, "OIDC_TOKEN_MODIFIED_FIELD", "updated_at")
OIDC_USER_UID = getattr(settings, "OIDC_USER_UID", "kc_id")
OIDC_USER_MAPPING = getattr(
    settings,
    "OIDC_USER_MAPPING",
    {
        "given_name": "first_name",
        "family_name": "last_name",
        "name": "username",
    },
)
OIDC_USER_DEFAULTS = getattr(
    settings,
    "OIDC_USER_DEFAULTS",
    {
        "is_active": True,
    },
)
OIDC_USER_ON_CREATE = getattr(
    settings,
    "OIDC_USER_ON_CREATE",
    None,
)
OIDC_USER_ON_UPDATE = getattr(
    settings,
    "OIDC_USER_ON_UPDATE",
    None,
)

OIDC_CONFIG_ROUTES = getattr(settings, "OIDC_CONFIG_ROUTES", None)
