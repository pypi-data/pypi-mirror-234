import datetime

from typing import Union


class BaseStorage(object):
    def init_session(self, document_id: str, dpop_proof: dict, attestation: dict):
        raise NotImplementedError()

    def is_connected(self) -> bool:
        raise NotImplementedError()

    def close(self) -> None:
        raise NotImplementedError()

    def add_dpop_proof_and_attestation(self, document_id, dpop_proof: dict, attestation: dict):
        raise NotImplementedError()

    def set_finalized(self, document_id: str):
        raise NotImplementedError()

    def update_request_object(self, document_id: str, request_object: dict) -> int:
        raise NotImplementedError()

    def update_response_object(self, nonce: str, state: str, response_object: dict) -> int:
        raise NotImplementedError()

    def get_trust_attestation(self, entity_id: str) -> Union[dict, None]:
        raise NotImplementedError()

    def get_trust_anchor(self, entity_id: str) -> Union[dict, None]:
        raise NotImplementedError()

    def has_trust_attestation(self, entity_id: str):
        raise NotImplementedError()

    def has_trust_anchor(self, entity_id: str):
        raise NotImplementedError()

    def add_trust_attestation(self, entity_id: str, attestation: list[str], exp: datetime) -> str:
        raise NotImplementedError()

    def add_trust_anchor(self, entity_id: str, entity_configuration: str, exp: datetime):
        raise NotImplementedError()

    def update_trust_attestation(self, entity_id: str, attestation: list[str], exp: datetime) -> str:
        raise NotImplementedError()

    def update_trust_anchor(self, entity_id: str, entity_configuration: dict, exp: datetime) -> str:
        raise NotImplementedError()

    def exists_by_state_and_session_id(self, state: str, session_id: str = "") -> bool:
        raise NotImplementedError()

    def get_by_state(self, state: str):
        raise NotImplementedError()

    def get_by_nonce_state(self, state: str, nonce: str):
        raise NotImplementedError()

    def get_by_state_and_session_id(self, state: str, session_id: str = ""):
        raise NotImplementedError()

    def get_by_session_id(self, session_id: str):
        raise NotImplementedError()

    # TODO: create add_or_update for all the write methods
    def add_or_update_trust_attestation(self, entity_id: str, attestation: list[str], exp: datetime) -> str:
        raise NotImplementedError()
