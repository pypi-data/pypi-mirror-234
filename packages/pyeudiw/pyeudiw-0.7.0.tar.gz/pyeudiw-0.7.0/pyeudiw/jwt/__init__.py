import binascii
import json
from typing import Union

import cryptojwt
from cryptojwt.exception import VerificationError
from cryptojwt.jwe.jwe import factory
from cryptojwt.jwe.jwe_ec import JWE_EC
from cryptojwt.jwe.jwe_rsa import JWE_RSA
from cryptojwt.jwk.jwk import key_from_jwk_dict
from cryptojwt.jws.jws import JWS as JWSec

from pyeudiw.jwk import JWK
from pyeudiw.jwk.exceptions import KidError
from pyeudiw.jwt.utils import unpad_jwt_header

DEFAULT_HASH_FUNC = "SHA-256"

DEFAULT_SIG_KTY_MAP = {
    "RSA": "RS256",
    "EC": "ES256"
}

DEFAULT_SIG_ALG_MAP = {
    "RSA": "RS256",
    "EC": "ES256"
}

DEFAULT_ENC_ALG_MAP = {
    "RSA": "RSA-OAEP",
    "EC": "ECDH-ES+A256KW"
}

DEFAULT_ENC_ENC_MAP = {
    "RSA": "A256CBC-HS512",
    "EC": "A256GCM"
}


class JWEHelper():
    def __init__(self, jwk: JWK):
        self.jwk = jwk

    def encrypt(self, plain_dict: Union[dict, str, int, None], **kwargs) -> str:
        _key = key_from_jwk_dict(self.jwk.as_dict())

        if isinstance(_key, cryptojwt.jwk.rsa.RSAKey):
            JWE_CLASS = JWE_RSA
        elif isinstance(_key, cryptojwt.jwk.ec.ECKey):
            JWE_CLASS = JWE_EC

        _payload: str | int | bytes = ""

        if isinstance(plain_dict, dict):
            _payload = json.dumps(plain_dict).encode()
        elif not plain_dict:
            _payload = ""
        elif isinstance(plain_dict, (str, int)):
            _payload = plain_dict
        else:
            _payload = ""

        _keyobj = JWE_CLASS(
            _payload,
            alg=DEFAULT_ENC_ALG_MAP[_key.kty],
            enc=DEFAULT_ENC_ENC_MAP[_key.kty],
            kid=_key.kid,
            **kwargs
        )

        if _key.kty == 'EC':
            # TODO - TypeError: key must be bytes-like
            return _keyobj.encrypt(cek=_key.public_key())
        else:
            return _keyobj.encrypt(key=_key.public_key())

    def decrypt(self, jwe: str) -> dict:
        try:
            jwe_header = unpad_jwt_header(jwe)
        except (binascii.Error, Exception) as e:
            raise VerificationError("The JWT is not valid")

        _alg = jwe_header.get("alg")
        _enc = jwe_header.get("enc")
        jwe_header.get("kid")

        _decryptor = factory(jwe, alg=_alg, enc=_enc)

        _dkey = key_from_jwk_dict(self.jwk.as_dict())
        msg = _decryptor.decrypt(jwe, [_dkey])

        try:
            msg_dict = json.loads(msg)
        except json.decoder.JSONDecodeError:
            msg_dict = msg
        return msg_dict


class JWSHelper:
    def __init__(self, jwk: Union[JWK, dict]):
        self.jwk = jwk
        if isinstance(jwk, dict):
            self.jwk = JWK(jwk)
        self.alg = DEFAULT_SIG_KTY_MAP[self.jwk.key.kty]

    def sign(
        self,
        plain_dict: Union[dict, str, int, None],
        protected: dict = {},
        **kwargs
    ) -> str:

        _key = key_from_jwk_dict(self.jwk.as_dict())

        _payload: str | int | bytes = ""

        if isinstance(plain_dict, dict):
            _payload = json.dumps(plain_dict).encode()
        elif not plain_dict:
            _payload = ""
        elif isinstance(plain_dict, (str, int)):
            _payload = plain_dict
        else:
            _payload = ""

        _signer = JWSec(_payload, alg=self.alg, **kwargs)
        return _signer.sign_compact([_key], protected=protected, **kwargs)

    def verify(self, jws: str, **kwargs):
        _key = key_from_jwk_dict(self.jwk.as_dict())
        _jwk_dict = self.jwk.as_dict()
        _head = unpad_jwt_header(jws)

        if _head.get("kid"):
            if _head["kid"] != _jwk_dict["kid"]:  # pragma: no cover
                raise KidError(
                    f"{_head.get('kid')} != {_jwk_dict['kid']}. Loaded/expected is {_jwk_dict}) while the verified JWS header is {_head}"
                )
        # TODO: check why unfortunately obtaining a public key from a TEE may dump a different y value using EC keys
        # elif _head.get("jwk"):
            # if _head["jwk"] != _jwk_dict:  # pragma: no cover
                # raise JwkError(
                # f"{_head['jwk']} != {_jwk_dict}"
                # )

        verifier = JWSec(alg=_head["alg"], **kwargs)
        msg = verifier.verify_compact(jws, [_key])
        return msg
