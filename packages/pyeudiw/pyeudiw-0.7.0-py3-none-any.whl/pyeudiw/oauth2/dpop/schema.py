from typing import Literal

from pydantic import BaseModel, HttpUrl


class DPoPTokenHeaderSchema(BaseModel):
    # header
    typ: Literal["dpop+jwt"]
    alg: Literal[
        "RS256",
        "RS384",
        "RS512",
        "ES256",
        "ES384",
        "ES512",
        "PS256",
        "PS384",
        "PS512",
    ]
    # TODO - dynamic schemas loader if EC or RSA
    # jwk: JwkSchema


class DPoPTokenPayloadSchema(BaseModel):
    # body
    jti: str
    htm: Literal["GET", "POST", "get", "post"]
    htu: HttpUrl
    iat: int
    ath: str
