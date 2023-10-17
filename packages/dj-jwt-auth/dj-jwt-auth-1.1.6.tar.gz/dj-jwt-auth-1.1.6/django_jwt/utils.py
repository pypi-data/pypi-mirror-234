import base64
import json
from functools import cache

import jwt
import requests
from jwt.algorithms import ECAlgorithm, RSAAlgorithm

from django_jwt import settings


def get_alg(token: str) -> str:
    header = json.loads(base64.b64decode(token.split(".")[0] + "==="))
    return header["alg"]


class Config:
    def __init__(self):
        self.route = settings.OIDC_CONFIG_ROUTES

    @cache
    def cfg(self, alg: str) -> dict:
        if self.route and alg in self.route:
            return requests.get(self.route[alg]).json()
        return requests.get(settings.OIDC_CONFIG_URL).json()

    @cache
    def get_public_key(self, alg: str) -> str:
        certs_data_response = requests.get(self.cfg(alg)["jwks_uri"])
        certs_data_response.raise_for_status()

        certs_data = certs_data_response.json()
        for key_data in certs_data["keys"]:
            if key_data["alg"] == alg:
                algorithm = RSAAlgorithm if key_data["kty"] == "RSA" else ECAlgorithm
                return algorithm.from_jwk(json.dumps(key_data))


_config = Config()


class OIDCHandler:
    def get_user_info(self, token: str) -> dict:
        alg = get_alg(token)
        url = _config.cfg(alg)["userinfo_endpoint"]
        response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        response.raise_for_status()
        return response.json()

    def decode_token(self, token: str) -> dict:
        alg = get_alg(token)
        public_key = _config.get_public_key(alg)
        if not public_key:
            raise Exception(f"Public key for {alg} not found")

        return jwt.decode(
            token,
            key=public_key,
            algorithms=[alg],
            audience=settings.OIDC_AUDIENCE,
            options={"verify_aud": False},
        )


oidc_handler = OIDCHandler()
