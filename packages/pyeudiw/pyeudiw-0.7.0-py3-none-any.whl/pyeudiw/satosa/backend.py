import base64
import datetime
import json
import hashlib
import logging
import uuid

from urllib.parse import quote_plus, urlencode

import satosa.logging_util as lu
from satosa.backends.base import BackendModule
from satosa.context import Context
from satosa.internal import AuthenticationInformation, InternalData
from satosa.response import Redirect, Response

from pyeudiw.jwk import JWK
from pyeudiw.jwt import JWSHelper
from pyeudiw.satosa.exceptions import (
    NotTrustedFederationError
)
from pyeudiw.satosa.dpop import BackendDPoP
from pyeudiw.satosa.html_template import Jinja2TemplateHandler
from pyeudiw.satosa.response import JsonResponse
from pyeudiw.satosa.trust import BackendTrust
from pyeudiw.tools.mobile import is_smartphone
from pyeudiw.tools.qr_code import QRCode
from pyeudiw.tools.utils import iat_now, exp_from_now
from pyeudiw.openid4vp.schemas.response import ResponseSchema
from pyeudiw.openid4vp.direct_post_response import DirectPostResponse
from pyeudiw.openid4vp.exceptions import (
    KIDNotFound,
    InvalidVPToken
)
from pyeudiw.storage.db_engine import DBEngine
from pyeudiw.storage.exceptions import StorageWriteError

from pydantic import ValidationError


logger = logging.getLogger(__name__)


class OpenID4VPBackend(BackendModule, BackendTrust, BackendDPoP):
    """
    A backend module (acting as a OpenID4VP SP).
    """

    def __init__(self, auth_callback_func, internal_attributes, config, base_url, name):
        """
        OpenID4VP backend module.
        :param auth_callback_func: Callback should be called by the module after the authorization
        in the backend is done.
        :param internal_attributes: Mapping dictionary between SATOSA internal attribute names and
        the names returned by underlying IdP's/OP's as well as what attributes the calling SP's and
        RP's expects namevice.
        :param config: Configuration parameters for the module.
        :param base_url: base url of the service
        :param name: name of the plugin
        :type auth_callback_func:
        (satosa.context.Context, satosa.internal.InternalData) -> satosa.response.Response
        :type internal_attributes: dict[string, dict[str, str | list[str]]]
        :type config: dict[str, dict[str, str] | list[str]]
        :type base_url: str
        :type name: str
        """
        super().__init__(auth_callback_func, internal_attributes, base_url, name)

        self.config = config
        self.client_id = self.config['metadata']['client_id']
        self.default_exp = int(self.config['jwt']['default_exp'])

        self.metadata_jwks_by_kids = {
            i['kid']: i for i in self.config['metadata_jwks']
        }

        self.config['metadata']['jwks'] = {"keys": [
            JWK(i).public_key for i in self.config['metadata_jwks']
        ]}

        # HTML template loader
        self.template = Jinja2TemplateHandler(self.config["ui"])

        # it will be filled by .register_endpoints
        self.absolute_redirect_url = None
        self.absolute_request_url = None
        self.absolute_status_url = None
        self.registered_get_response_endpoint = None

        # resolve metadata pointers/placeholders
        self._render_metadata_conf_elements()
        self.init_trust_resources()

        logger.debug(
            lu.LOG_FMT.format(
                id="OpenID4VP init",
                message=f"Loaded configuration: {json.dumps(config)}"
            )
        )

    @property
    def db_engine(self) -> DBEngine:

        try:
            self._db_engine.is_connected
        except Exception as e:
            if getattr(self, '_db_engine', None):
                logger.debug(
                    lu.LOG_FMT.format(
                        id="OpenID4VP db storage handling",
                        message=f"connection check silently fails and get restored: {e}"
                    )
                )
            self._db_engine = DBEngine(self.config["storage"])

        return self._db_engine

    def _render_metadata_conf_elements(self) -> None:
        for k, v in self.config['metadata'].items():
            if isinstance(v, (int, float, dict, list)):
                continue
            if not v or len(v) == 0:
                continue
            if all((
                v[0] == '<',
                v[-1] == '>',
                '.' in v
            )):
                conf_section, conf_k = v[1:-1].split('.')
                self.config['metadata'][k] = self.config[conf_section][conf_k]

    @property
    def default_metadata_private_jwk(self) -> tuple:
        return tuple(self.metadata_jwks_by_kids.values())[0]

    def register_endpoints(self) -> list:
        """
        Creates a list of all the endpoints this backend module needs to listen to. In this case
        it's the authentication response from the underlying OP that is redirected from the OP to
        the proxy.
        :rtype: Sequence[(str, Callable[[satosa.context.Context], satosa.response.Response]]
        :return: A list that can be used to map the request to SATOSA to this endpoint.
        """
        url_map = []
        for k, v in self.config['endpoints'].items():
            url_map.append(
                (
                    f"^{self.name}/{v.lstrip('/')}$",
                    getattr(self, f"{k}_endpoint")
                )
            )
            _endpoint = f"{self.client_id}{v}"
            logger.debug(
                f"Exposing backend entity endpoint = {_endpoint}"
            )
            if k == 'get_response':
                self.registered_get_response_endpoint = _endpoint
            elif k == 'redirect':
                self.absolute_redirect_url = _endpoint
            elif k == 'request':
                self.absolute_request_url = _endpoint
            elif k == "status":
                self.absolute_status_url = _endpoint
        return url_map

    def start_auth(self, context, internal_request):
        """
        This is the start up function of the backend authorization.

        :type context: satosa.context.Context
        :type internal_request: satosa.internal.InternalData
        :rtype satosa.response.Response

        :param context: the request context
        :param internal_request: Information about the authorization request
        :return: response
        """
        return self.pre_request_endpoint(context, internal_request)

    def _log(self, context: Context, level: str, message: str) -> None:
        log_level = getattr(logger, level)
        log_level(
            lu.LOG_FMT.format(
                id=lu.get_session_id(context.state),
                message=message
            )
        )

    def pre_request_endpoint(self, context, internal_request, **kwargs):

        self._log(
            context,
            level='debug',
            message=(
                "[INCOMING REQUEST] pre_request_endpoint with Context: "
                f"{context.__dict__} and internal_request: {internal_request}"
            )
        )

        session_id = context.state["SESSION_ID"]
        state = str(uuid.uuid4())

        # TODO: do not init the session if the context is not linked to any
        #       previous authn session (avoid to init sessions for users that has not requested an auth to a frontend)

        # Init session
        try:
            self.db_engine.init_session(
                state=state,
                session_id=session_id
            )
        except (Exception, StorageWriteError) as e:
            _msg = (
                f"Error while initializing session with state {state} and {session_id}. "
            )
            return self.handle_error(
                context,
                message="server_error",
                troubleshoot=f"{_msg}",
                err=f"{_msg}. {e.__class__.__name__}: {e}",
                err_code="500"
            )

        # PAR
        payload = {
            'client_id': self.client_id,
            'request_uri': f"{self.absolute_request_url}?id={state}",
        }
        url_params = urlencode(payload, quote_via=quote_plus)

        if is_smartphone(context.http_headers.get('HTTP_USER_AGENT')):
            # Same Device flow
            res_url = f'{self.config["authorization"]["url_scheme"]}://authorize?{url_params}'
            return Redirect(res_url)

        # Cross Device flow
        res_url = f'{self.client_id}?{url_params}'
        encoded_res_url = base64.urlsafe_b64encode(res_url.encode())

        # response = base64.b64encode(res_url.encode())
        qrcode = QRCode(encoded_res_url, **self.config['qrcode'])

        result = self.template.qrcode_page.render(
            {
                'qrcode_base64': qrcode.to_base64(),
                "state": state,
                "status_endpoint": self.absolute_status_url
            }
        )
        return Response(result, content="text/html; charset=utf8", status="200")

    def _translate_response(self, response: dict, issuer: str, context: Context):
        """
        Translates wallet response to SATOSA internal response.
        :type response: dict[str, str]
        :type issuer: str
        :type subject_type: str
        :rtype: InternalData
        :param response: Dictioary with attribute name as key.
        :param issuer: The oidc op that gave the repsonse.
        :param subject_type: public or pairwise according to oidc standard.
        :return: A SATOSA internal response.
        """
        # it may depends by credential type and attested security context evaluated
        # if WIA was previously submitted by the Wallet

        timestamp_epoch = (
            response.get("auth_time")
            or response.get("iat")
            or iat_now()
        )
        timestamp_dt = datetime.datetime.fromtimestamp(
            timestamp_epoch,
            datetime.timezone.utc
        )
        timestamp_iso = timestamp_dt.isoformat().replace("+00:00", "Z")

        auth_class_ref = (
            response.get("acr") or
            response.get("amr") or
            self.config["authorization"]["default_acr_value"]
        )
        auth_info = AuthenticationInformation(
            auth_class_ref, timestamp_iso, issuer)

        # TODO - ACR values
        internal_resp = InternalData(auth_info=auth_info)

        sub = ""
        for i in self.config["user_attributes"]["unique_identifiers"]:
            if response.get(i):
                _sub = response[i]
                sub = hashlib.sha256(
                    f"{_sub}~{self.config['user_attributes']['subject_id_salt']}".encode(
                    )
                ).hexdigest()
                break

        if not sub:
            self._log(
                context,
                level='warning',
                message=(
                    "[USER ATTRIBUTES] Missing subject id from OpenID4VP presentation "
                    "setting a random one for interop for internal frontends"
                )
            )
            # TODO - add a salt here
            sub = hashlib.sha256(
                json.dumps(response).encode()
            ).hexdigest()

        response["sub"] = [sub]
        internal_resp.attributes = self.converter.to_internal(
            "openid4vp", response
        )
        internal_resp.subject_id = sub
        return internal_resp

    @property
    def server_url(self):
        return (
            self.base_url[:-1]
            if self.base_url[-1] == '/'
            else self.base_url
        )

    def redirect_endpoint(self, context, *args):
        self._log(
            context,
            level='debug',
            message=(
                "[INCOMING REQUEST] redirect_endpoint with Context: "
                f"{context.__dict__} and args: {args}"
            )
        )
        if context.request_method.lower() != 'post':
            # raise BadRequestError("HTTP Method not supported")
            return self.handle_error(
                context=context,
                message="invalid_request",
                troubleshoot="HTTP Method not supported",
                err_code="400"
            )

        _endpoint = f'{self.server_url}{context.request_uri}'
        if self.config["metadata"].get('redirect_uris', None):
            if _endpoint not in self.config["metadata"]['redirect_uris']:
                return self.handle_error(
                    context=context,
                    message="invalid_request",
                    troubleshoot="request_uri not valid",
                    err_code="400"
                )

        # take the encrypted jwt, decrypt with my public key (one of the metadata) -> if not -> exception
        jwt = context.request.get("response", None)
        if not jwt:
            _msg = f"Response error, missing JWT"
            self._log(context, level='error', message=_msg)
            return self.handle_error(
                context=context,
                message="invalid_request",
                troubleshoot=_msg,
                err_code="400"
            )

        try:
            vpt = DirectPostResponse(jwt, self.metadata_jwks_by_kids)
            self._log(
                context,
                level='debug',
                message=(
                    f"Redirect uri endpoint Response using direct post contains: {vpt.payload}"
                )
            )
            ResponseSchema(**vpt.payload)
        except Exception as e:
            _msg = f"DirectPostResponse parse and validation error: {e}"
            self._log(context, level='error', message=_msg)
            return self.handle_error(
                context=context,
                message="invalid_request",
                troubleshoot=_msg,
                err_code="400",
                err=f"Error:{e}, with JWT: {jwt}"
            )

        # state MUST be present in the response since it was in the request
        # then do lookup on the db -> if not -> exception
        state = vpt.payload.get("state", None)
        if not state:
            return self.handle_error(
                context=context,
                message="invalid_request",
                troubleshoot="state not found in the response",
                err_code="400",
                err=f"{_msg} with: {vpt.payload}"
            )

        try:
            stored_session = self.db_engine.get_by_state(state=state)
        except Exception as e:
            _msg = f"Session lookup by state value failed"
            return self.handle_error(
                context=context,
                message="invalid_request",
                troubleshoot=_msg,
                err=f"{e.__class__.__name__}: {e}",
                err_code="400"
            )
        
        if stored_session["finalized"]:
            _msg = f"Session already finalized"
            return self.handle_error(
                context=context,
                message="invalid_request",
                troubleshoot=_msg,
                err=_msg,
                err_code="400"
            )
        
        # TODO: handle vp token ops exceptions
        try:
            vpt.load_nonce(stored_session['nonce'])
            vps: list = vpt.get_presentation_vps()
            vpt.validate()
        except Exception as e:
            _msg = (
                "DirectPostResponse content parse and validation error. "
                f"Single VPs are faulty."
            )
            return self.handle_error(
                context=context,
                message="invalid_request",
                troubleshoot=_msg,
                err=f"{e.__class__.__name__}: {e}",
                err_code="400"
            )

        # evaluate the trust to each credential issuer found in the vps
        # look for trust chain or x509 or do discovery!
        cred_issuers = tuple(vpt.credentials_by_issuer.keys())
        attributes_by_issuers = {k: {} for k in cred_issuers}

        for vp in vps:
            try:
                # establish the trust with the issuer of the credential by checking it to the revocation
                # inspect VP's iss or trust_chain if available or x5c if available
                # TODO: X.509 as alternative to Federation

                # for each single vp token, take the credential within it, use cnf.jwk to validate the vp token signature -> if not exception
                # establish the trust to each credential issuer
                tchelper = self._validate_trust(context, vp.payload['vp'])

                if not tchelper.is_trusted:
                    return self.handle_error(
                        context=context,
                        message="invalid_request",
                        troubleshoot=f"Trust Evaluation failed for {tchelper.entity_id}",
                        err_code="400"
                    )

                # TODO: generalyze also for x509
                vp.credential_jwks = tchelper.get_trusted_jwks(
                    metadata_type='openid_credential_issuer'
                )
            except InvalidVPToken:
                return self.handle_error(context=context, message="invalid_request", troubleshoot=f"Cannot validate VP: {vp.jwt}", err_code="400")
            except ValidationError as e:
                return self.handle_error(context=context, message="invalid_request", troubleshoot=f"Error validating schemas: {e}", err_code="400")
            except KIDNotFound as e:
                return self.handle_error(context=context, message="invalid_request", troubleshoot=f"Kid error: {e}", err_code="400")
            except NotTrustedFederationError as e:
                return self.handle_error(context=context, message="invalid_request", troubleshoot=f"Not trusted federation error: {e}", err_code="400")
            except Exception as e:
                return self.handle_error(context=context, message="invalid_request", troubleshoot=f"VP parsing error: {e}", err_code="400")

            # the trust is established to the credential issuer, then we can get the disclosed user attributes
            # TODO - what if the credential is different from sd-jwt? -> generalyze within Vp class
            
            try:
                vp.verify_sdjwt(
                    issuer_jwks_by_kid={i['kid']: i for i in vp.credential_jwks}
                )
            except Exception as e:
                return self.handle_error(
                    context=context, 
                    message="invalid_request", 
                    troubleshoot=f"VP SD-JWT validation error: {e}", 
                    err_code="400"
                )

            # vp.result
            attributes_by_issuers[vp.credential_issuer] = vp.disclosed_user_attributes
            self._log(
                context,
                level='debug',
                message=f"Disclosed user attributes from {vp.credential_issuer}: {vp.disclosed_user_attributes}"
            )

            # TODO: check the revocation of the credential
            # ...

        # for all the valid credentials, take the payload and the disclosure and disclose user attributes
        # returns the user attributes ...
        all_user_attributes = dict()
        for i in attributes_by_issuers.values():
            all_user_attributes.update(**i)

        self._log(
            context, level='debug',
            message=f"Wallet disclosure: {all_user_attributes}"
        )

        # TODO: not sure that we want these issuers in the following form ... please recheck.
        _info = {"issuer": ';'.join(cred_issuers)}
        internal_resp = self._translate_response(
            all_user_attributes, _info["issuer"], context
        )

        try:
            self.db_engine.update_response_object(
                stored_session['nonce'], state, internal_resp
            )
            # authentication finalized!
            self.db_engine.set_finalized(stored_session['document_id'])
            if logger.getEffectiveLevel() == logging.DEBUG:
                stored_session = self.db_engine.get_by_state(state=state)
                self._log(
                    context,
                    level="debug",
                    message=f"Session update on storage: {stored_session}"
                )
        except StorageWriteError as e:
            # TODO - do we have to block in the case the update cannot be done?
            self._log(
                context,
                level="error",
                message=f"Session update on storage failed: {e}"
            )
            return self.handle_error(
                context=context,
                message="server_error",
                troubleshoot=f"Cannot update response object.",
                err=f"{e.__class__.__name__}: {e}",
                err_code="500"
            )

        if stored_session['session_id'] == context.state["SESSION_ID"]:
            # Same device flow
            return Redirect(
                self.registered_get_response_endpoint
            )
        else:
            # Cross device flow
            return JsonResponse(
                {
                    "status": "OK"
                },
                status="200"
            )

    def request_endpoint(self, context, *args):

        self._log(
            context,
            level='debug',
            message=(
                "[INCOMING REQUEST] request_endpoint with Context: "
                f"{context.__dict__} and args: {args}"
            )
        )
        # check DPOP for WIA if any
        try:
            dpop_validation_error: JsonResponse = self._request_endpoint_dpop(
                context
            )
            if dpop_validation_error:
                return dpop_validation_error
        except Exception as e:
            _msg = (
                f"[DPoP VALIDATION ERROR] WIA evalution error: {e}."
            )
            return self.handle_error(
                context=context,
                message="invalid_client",
                troubleshoot=_msg,
                err=f"{e} with {context.__dict__}",
                err_code="401"
            )

        try:
            state = context.qs_params["id"]
        except Exception as e:
            _msg = (
                "Error while retrieving id from qs_params: "
                f"{e.__class__.__name__}: {e}"
            )
            return self.handle_error(
                context,
                message="invalid_request",
                troubleshoot=_msg,
                err=f"{e} with {context.__dict__}",
                err_code="400"
            )

        data = {
            "scope": ' '.join(self.config['authorization']['scopes']),
            "client_id_scheme": "entity_id",  # that's federation.
            "client_id": self.client_id,
            "response_mode": "direct_post.jwt",  # only HTTP POST is allowed.
            "response_type": "vp_token",
            "response_uri": self.absolute_redirect_url,
            "nonce": str(uuid.uuid4()),
            "state": state,
            "iss": self.client_id,
            "iat": iat_now(),
            # TODO: set an exp for the request in the general conf
            "exp": exp_from_now(minutes=5)
        }

        try:
            dpop_proof = context.http_headers['HTTP_DPOP']
            attestation = context.http_headers['HTTP_AUTHORIZATION']
        except KeyError as e:
            _msg = f"Error while accessing http headers: {e}"
            return self.handle_error(
                context,
                message="invalid_request",
                err=f"{e} with {context.__dict__}",
                err_code="400"
            )

        # take the session created in the pre-request authz endpoint
        try:
            document = self.db_engine.get_by_state(state)
            document_id = document["document_id"]
            self.db_engine.add_dpop_proof_and_attestation(
                document_id, dpop_proof, attestation
            )
            self.db_engine.update_request_object(document_id, data)
        except ValueError as e:
            _msg = (
                "Error while retrieving request object from database."
            )
            return self.handle_error(
                context,
                message="server_error",
                troubleshoot=_msg,
                err=f"{e} with {context.__dict__}",
                err_code="500"
            )
        except (Exception, BaseException) as e:
            _msg = f"Error while updating request object: {e}"
            return self.handle_error(
                context,
                message="server_error",
                err=_msg,
                err_code="500"
            )

        helper = JWSHelper(self.default_metadata_private_jwk)

        jwt = helper.sign(
            data,
            protected={'trust_chain': self.my_trust_chain}
        )
        response = {"response": jwt}

        # TODO: update the storage with the acquired signed request object
        return JsonResponse(
            response,
            status="200"
        )

    def handle_error(
        self,
        context: dict,
        message: str,
        troubleshoot: str = "",
        err="",
        err_code="500",
        template_path="templates",
        error_template="error.html",
        level="error"
    ):

        # TODO: evaluate with UX designers if Jinja2 template
        # loader and rendering is required, it seems not.

        _msg = f"{message}:"
        if err:
            _msg += f" {err}."
        self._log(
            context, level=level,
            message=f"{_msg} {troubleshoot}"
        )

        return JsonResponse(
            {
                "error": message,
                "error_description": troubleshoot
            },
            status=err_code
        )

    def get_response_endpoint(self, context):

        self._log(
            context,
            level='debug',
            message=(
                "[INCOMING REQUEST] get_response_endpoint with Context: "
                f"{context.__dict__}"
            )
        )

        state = context.qs_params.get("id", None)
        session_id = context.state["SESSION_ID"]
        finalized_session = None

        try:
            if state:
                # cross device
                finalized_session = self.db_engine.get_by_state_and_session_id(
                    state=state, session_id=session_id
                )
            else:
                # same device
                finalized_session = self.db_engine.get_by_session_id(
                    session_id=session_id
                )
        except Exception as e:
            _msg = f"Error while retrieving session by state {state} and session_id {session_id}: {e}"
            return self.handle_error(
                context=context,
                message="invalid_client",
                troubleshoot=_msg,
                err_code="401"
            )

        if not finalized_session:
            return self.handle_error(
                context=context,
                message="invalid_request",
                troubleshoot="session not found or invalid",
                err_code="400"
            )
        
        _now = iat_now()
        _exp = finalized_session['request_object']['exp']
        if _exp < _now:
            return self.handle_error(
                context=context,
                message="invalid_request",
                troubleshoot=f"session expired, request object exp is {_exp} while now is {_now}",
                err_code="400"
            )
        
        internal_response = InternalData()
        resp = internal_response.from_dict(
            finalized_session['internal_response']
        )

        return self.auth_callback_func(
            context,
            resp
        )

    def status_endpoint(self, context):

        self._log(
            context,
            level='debug',
            message=(
                "[INCOMING REQUEST] state_endpoint with Context: "
                f"{context.__dict__}"
            )
        )

        session_id = context.state["SESSION_ID"]
        _err_msg = ""
        state = None

        try:
            state = context.qs_params["id"]
        except TypeError as e:
            _err_msg = f"No query params found: {e}"
        except KeyError as e:
            _err_msg = f"No id found in qs_params: {e}"

        if _err_msg:
            return self.handle_error(
                context=context,
                message="invalid_request",
                troubleshoot=_err_msg,
                err_code="400"
            )

        try:
            session = self.db_engine.get_by_state_and_session_id(
                state=state, session_id=session_id
            )
        except Exception as e:
            _msg = f"Error while retrieving session by state {state} and session_id {session_id}: {e}"
            return self.handle_error(
                context=context,
                message="invalid_client",
                troubleshoot=_msg,
                err_code="401"
            )

        # TODO: if the request is expired -> return 403
        if session["finalized"]:
            #  return Redirect(
            #      self.registered_get_response_endpoint
            #  )
            return JsonResponse(
                {
                    "response_url": f"{self.registered_get_response_endpoint}?id={state}"
                },
                status="200"
            )
        else:
            return JsonResponse(
                {
                    "response": "Request object issued"
                },
                status="201"
            )
