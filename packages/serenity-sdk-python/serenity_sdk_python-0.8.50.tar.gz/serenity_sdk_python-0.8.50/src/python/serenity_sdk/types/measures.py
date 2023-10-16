from datetime import datetime
from serenity_types.utils.serialization import CamelModel
from serenity_types.risk.measures import RiskComputationRequest


class RiskMeasureContext(CamelModel):
    """
    The context for the risk measure computation.
    """

    request: RiskComputationRequest
    "The request that generated the response"
    as_of_time: datetime
    "The date and time of the reference data for the risk measures"
