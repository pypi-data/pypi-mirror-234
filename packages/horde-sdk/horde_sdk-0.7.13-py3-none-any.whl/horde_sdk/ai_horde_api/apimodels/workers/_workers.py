
from typing_extensions import override

from horde_sdk.ai_horde_api.apimodels.base import BaseAIHordeRequest
from horde_sdk.ai_horde_api.endpoints import AI_HORDE_API_ENDPOINT_SUBPATH
from horde_sdk.ai_horde_api.fields import TeamID
from horde_sdk.consts import HTTPMethod
from horde_sdk.generic_api.apimodels import (
    APIKeyAllowedInRequestMixin,
    HordeResponse,
)


class WorkerModifyResponse(HordeResponse):
    @override
    @classmethod
    def get_api_model_name(cls) -> str | None:
        return "ModifyWorkerInput"


class WorkerModifyRequest(BaseAIHordeRequest, APIKeyAllowedInRequestMixin):
    """Returns information on all works. If a moderator API key is specified, it will return additional information."""

    """ModifyWorkerInput{
    maintenance	boolean
    Set to true to put this worker into maintenance.

    maintenance_msg	string
    if maintenance is True, you can optionally provide a message to be used instead of the default maintenance message, so that the owner is informed.

    paused	boolean
    (Mods only) Set to true to pause this worker.

    info	string
    minLength: 2
    maxLength: 1000
    You can optionally provide a server note which will be seen in the server details. No profanity allowed!

    name	string
    minLength: 5
    maxLength: 100
    When this is set, it will change the worker's name. No profanity allowed!

    team	string
    example: 0bed257b-e57c-4327-ac64-40cdfb1ac5e6
    maxLength: 36
    The team towards which this worker contributes kudos. It an empty string ('') is passed, it will leave the worker without a team. No profanity allowed!

    }"""

    maintenance: bool | None = None
    maintenance_msg: str | None = None
    paused: bool | None = None
    info: str | None = None
    name: str | None = None
    team: TeamID | None = None

    @override
    @classmethod
    def get_api_model_name(cls) -> str | None:
        return None

    @override
    @classmethod
    def get_api_endpoint_subpath(cls) -> AI_HORDE_API_ENDPOINT_SUBPATH:
        return AI_HORDE_API_ENDPOINT_SUBPATH.v2_workers

    @override
    @classmethod
    def get_http_method(cls) -> HTTPMethod:
        return HTTPMethod.PUT

    @override
    @classmethod
    def get_default_success_response_type(cls) -> type[HordeResponse]:
        return WorkerModifyResponse
