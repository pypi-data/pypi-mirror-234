from datetime import datetime
from pydantic import Field
from serenity_types.refdata.derivatives import ListedDerivative, PayoffType, Expiry


class Future(ListedDerivative):
    """
    An exchange-listed futures contract.
    """

    expiry: Expiry = Field(
        deprecated=True,
        description="(DEPRECATED) Refers to expiry_datetime instead"
    )

    expiry_datetime: datetime
    """
    Expiration datetime for this particular term futures contract.
    """

    payoff_type: PayoffType
    """
    Whether the contract tracks the price movement (LINEAR) or its mirror image (INVERSE).
    """


class Perpetual(ListedDerivative):
    """
    An exchange-listed perpetual future, sometimes referred to as a swap.
    """

    payoff_type: PayoffType
    """
    Whether the contract tracks the price movement (LINEAR) or its mirror image (INVERSE).
    """
