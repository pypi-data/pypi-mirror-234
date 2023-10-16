from datetime import date, datetime
from typing import Generic, List, Optional, TypeVar
from pydantic import Field, BaseModel
from uuid import UUID
from pydantic.generics import GenericModel
from serenity_types.utils.serialization import CamelModel

T = TypeVar('T', bound=BaseModel)


class Response(CamelModel, GenericModel, Generic[T]):
    """
    Generic response wrapper that conforms to the Serenity REST standard. The result
    object is the payload in the response and can vary from endpoint to endpoint.
    The other fields are used to convey supporting information like warnings generated
    by the system in response to the request, e.g. if missing data was skipped.

    In some cases we will do some on-the-fly JSON object rewriting to force API
    output into this shape pre-decoding, as the current API is not 100% consistent.
    """

    request_id: UUID
    """
    The correlated request ID for this response.
    """

    as_of_date: Optional[date] = Field(
        deprecated=True,
        description="(DEPRECATED) Refer to as_of_time instead."
    )
    """
    For reference data and other requests that are loaded for a milestone "as-of" date,
    the date that was loaded. In cases where the inbound request took the default and
    did not pass in an as_of_date this lets the client know the latest date loaded.
    """

    as_of_time: Optional[datetime]
    """
    For reference data and other requests that are loaded for a milestone "as-of" datetime,
    the datetime that was loaded. In cases where the inbound request took the default and
    did not pass in an as_of_time this lets the client know the latest datetime loaded.
    """

    warnings: Optional[List[str]]
    """
    Any warnings from the analytics or data layer to qualify the response. Some API's
    going forward will support a 'strict' mode which does not tolerate warnings.
    """

    result: T
    """
    The response payload; can be anything but typically another Pydantic custom type.
    """
