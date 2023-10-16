from abc import ABC
from datetime import date, datetime
from typing import Any, Dict, Optional, TypeVar, Union
from uuid import UUID

from serenity_sdk.client.config import Environment
from serenity_sdk.client.raw import CallType, SerenityClient
from serenity_sdk.types.common import STD_DATE_FMT, STD_DATETIME_FMT
from serenity_types.utils.common import Response

T = TypeVar('T')


class SerenityApi(ABC):
    """
    Higher-level wrapper around a particular API endpoint like the Risk API or Model API. Subclasses
    add typed operations and various helper functions specific to that API group.
    """
    def __init__(self, client: SerenityClient, api_group: str):
        """
        :param client: the raw client to delegate to when making API calls
        :param api_group: the specific API group to target, e.g. risk or refdata
        """
        self.client = client
        self.api_group = api_group

    def _call_api(self, api_path: str, params: Dict[str, Any] = {}, body_json: Any = None,
                  call_type: CallType = CallType.GET) -> Any:
        """
        Helper method for derived classes that calls a target API in the supported API group.

        :param api_path: the target API path, excluding version prefix and API group (e.g. `/v1/risk`)
        :param params: the GET-style parameters to pass through to the raw client
        :param body_json: a raw JSON object to POST or PATCH via the raw client
        :return: the raw JSON response object
        """
        return self.client.call_api(self.api_group, api_path, params, body_json, call_type)

    def _get_env(self) -> Environment:
        """
        Internal helper to get the current API environment (dev, test, production).

        :return: the currently-connected environment
        """
        return self.client.env

    @staticmethod
    def _create_std_params(as_of_datetime: Optional[Union[date, datetime]]) -> Dict[str, str]:
        """
        Internal helper that generates params dict based on common parameters for Model API.

        :param as_of_datetime: the universal as_of_datetime for all bitemporal API's
        """
        if as_of_datetime is None:
            return {}
        elif isinstance(as_of_datetime, datetime):
            return {'asOfTime': as_of_datetime.strftime(STD_DATETIME_FMT)}
        else:
            return {'asOfDate': as_of_datetime.strftime(STD_DATE_FMT)}

    @staticmethod
    def _create_response_object(raw_json: Dict[str, Any], result: T) -> Response[T]:
        request_id = UUID(raw_json.get('requestId', raw_json.get('request_id')))
        as_of_date = datetime.strptime(raw_json.get('asOfDate', raw_json.get('as_of_date')), STD_DATE_FMT)
        warnings = raw_json.get('warnings', [])
        response = Response[T](
            request_id=request_id,
            as_of_date=as_of_date,
            warnings=warnings,
            result=result)
        return response
