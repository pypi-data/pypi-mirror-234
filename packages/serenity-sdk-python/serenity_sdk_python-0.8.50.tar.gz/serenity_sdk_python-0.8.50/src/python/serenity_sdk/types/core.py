
from uuid import UUID

from serenity_types.utils.serialization import CamelModel


class PortfolioAccountBalanceRequest(CamelModel):
    """
    Input for the balance fetching request
    """

    metadata_id: UUID
    """
    Unique identifier for the porfolio.
    """
