from typing import Optional
from uuid import UUID

from serenity_types.utils.serialization import CamelModel


class Balance(CamelModel):
    """
    The asset held in the portfolio at a specific point in time
    """

    quantity: float
    """
    The number of tokens, shares, contracts, etc. held in this position.
    If positive this indicates a long position; if negative, a short one.
    """

    asset_id: UUID
    """
    Unique identifier of the asset from Serenity's asset master database.
    """

    account_id: Optional[UUID]
    """
    Unique identifier of the account for transaction information.
    """
