from datetime import datetime
from enum import Enum, auto
from typing import Optional
from uuid import UUID
from serenity_types.utils.serialization import CamelModel


class AccountSource(CamelModel):
    """
    The authoritative source where trading activities, positions and balances can be found.
    """

    source_identifier: str
    """
    The unique identifier that matches to the account name in an exchange or a wallet address if it's in blockchain.
    """

    source_platform_id: UUID
    """
    The platform or source where the `source_identifier` is located. E.g. Binance, Coinbase, Ethereum blockchain.
    """


class Account(CamelModel):
    """
    Maintains the overall account information.
    """

    account_id: UUID
    """
    Unique and immutable ID.
    """

    version: int
    """
    Monotonically increasing version number.
    """

    owner: str
    """
    The primary owner of this account.
    """

    updated_by: str
    """
    Last update user.
    """

    updated_at: datetime
    """
    Last update timestamp, in UTC.
    """

    name: str
    """
    A descriptive name for this account.
    """

    account_source: AccountSource
    """
    The authoritative source where trading activities, positions and balances can be found.
    """

    connector_id: Optional[UUID]
    """
    The `PositionConnector` which created this account.
    Account created by `PositionConnector` cannot be manually removed or modified.
    """


class AccountBaseRequest(CamelModel):
    """
    The account base request class
    """
    name: str
    owner: str
    updated_by: str
    account_source: AccountSource


class AccountCreationRequest(AccountBaseRequest):
    """
    Input for the create request
    """
    pass


class AccountUpdateRequest(AccountBaseRequest):
    """
    Input for the update request
    """
    pass


class SourcePlatformType(Enum):
    """
    Enum classifying the source platform type, e.g. a central exchange, a digital wallet, etc.
    """

    def _generate_next_value_(name, start, count, last_values):
        return name

    EXCHANGE = auto()
    """
    Represents an account in an exchange.
    """

    WALLET = auto()
    """
    Represents a wallet address in an blockchain.
    """

    CUSTODIAN = auto()
    """
    Represents an account in a custodian.
    """

    CUSTODY_PROVIDER = auto()
    """
    Represents an account in a custody provider.
    """

    OTHER = auto()
    """
    Other type that is not available in the predefined list.
    """


class SourcePlatform(CamelModel):
    """
    The platform where user's position can be retrieved, such as a central exchange,
    wallet in blockchain, custodian, etc.
    """

    platform_type: SourcePlatformType
    """
    The source platform type, e.g an exchange, wallet in blockchain or other types.
    """

    platform_id: UUID
    """
    Unique ID for this platform.
    """

    display_name: str
    """
    Human-friendly name for this platform, e.g. Binance, Coinbase Prime, Ethereum.
    """

    xref: str
    """
    The reference used to determine the internal connectors to use.
    """

    provider_id: UUID
    """
    Unique ID for the provider of a platform.
    """

    provider_name: str
    """
    The literal name of the provider of a platform.
    """

    tags: Optional[dict]
    """
    Additional custom attributes that provide extra information beyond the default fields.
    """
