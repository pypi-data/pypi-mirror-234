from datetime import date
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import Field, validator
from serenity_types.refdata.symbology import SymbolAuthority
from serenity_types.utils.serialization import CamelModel


class AssetType(Enum):
    """
    Simple classification of assets.
    """

    CURRENCY = 'CURRENCY'
    """
    Fiat currency, e.g. EUR.
    """

    TOKEN = 'TOKEN'
    """
    Generic tokenized assets.
    """

    PEGGED_TOKEN = 'PEGGED_TOKEN'
    """
    A tokenized asset whose price is linked to an exposure.
    """

    WRAPPED_TOKEN = 'WRAPPED_TOKEN'
    """
    A tokenized asset which represents a claim on a token, typically on another Network.
    """

    FUTURE = 'FUTURE'
    """
    An exchange-listed futures contract.
    """

    PERPETUAL = 'PERPETUAL'
    """
    An exchange-listed perpetual future, a.k.a. swap.
    """

    LISTED_OPTION = 'LISTED_OPTION'
    """
    An exchange-listed option.
    """

    OTC_OPTION = 'OTC_OPTION'
    """
    An OTC option contract.
    """

    INDEX = 'INDEX'
    """
    A basket of other assets.
    """

    STRATEGY = 'STRATEGY'
    """
    A multi-leg asset composed of positions in other assets.
    """


class AssetStatus(Enum):
    """
    Asset status classification.
    """
    ACTIVE = 'ACTIVE'
    EXPIRED = 'EXPIRED'
    UNLISTED = 'UNLISTED'
    DELISTED = 'DELISTED'


class Asset(CamelModel):
    """
    Base class for all financial assets tracked in Serenity.
    """

    asset_id: UUID
    """
    Unique, immutable ID for this asset. Symbols can change over time,
    but asset ID's are stable.
    """

    is_supported: bool
    """
    Flag to indicate if this asset is supported by Serenity.
    """

    asset_status: AssetStatus
    """
    Asset status.
    """

    asset_type: AssetType
    """
    Basic classification of this asset. Based on the type, sub-classes of
    the Asset may carry additional details.
    """

    symbol: str
    """
    Serenity's unique symbol for this asset, e.g. tok.usdc.ethereum.
    """

    native_symbol: Optional[str]
    """
    Whatever is the issuer's symbol for this asset. For tokens this is typically the token smart contract symbol
    or native blockchain token symbol, e.g. ETH or DAI.
    """

    display_name: str
    """
    Human-readable name for this asset.
    """


class UnsupportedAsset(CamelModel):
    """
    The asset held in the portfolio but not currently supported.
    """

    contract_address: Optional[str]
    """
    The address of a contract held in this position.
    """

    symbol: Optional[str]
    """
    The symbol of a contract held in this position.
    """

    quantity: float
    """
    The number of contracts held in this position.
    """

    account_id: Optional[UUID]
    """
    Unique identifier of the account for transaction information.
    """


class XRefSymbol(CamelModel):
    """
    Legacy representation of a cross-reference symbol for an AssetSummary.
    """

    authority: SymbolAuthority
    """
    Symbology for which this symbol is authoritative, e.g. COINGECKO or SEDOL.
    """

    symbol: str
    """
    String symbol in the given symbology as of the effective date loaded.
    Note the vendor symbols can and do change over time, so this should
    be mapped to a Serenity asset ID using inputs from the same day.
    """


class AssetSummary(CamelModel):
    """
    Flattened, lowest common denominator representation of assets. This is to
    support the legacy Refdata API, which only handled TOKEN and CURRENCY.
    We will be replacing this with a richer mechanism going forward.
    """
    asset_id: UUID
    """
    Serenity's unique internal identifier for this asset. This never changes.
    """

    asset_type: AssetType
    """
    Serenity's classification for this asset, e.g. TOKEN or CURRENCY.
    """

    asset_symbol: str
    """
    Serenity's human-readable symbol for this asset. This identifier may change.
    """

    native_symbol: str
    """
    The blockchain, listing exchange or other primary authority's symbol, e.g. BTC.
    """

    display_name: str
    """
    Serenity's human-readable display name for this asset, e.g. Bitcoin.
    """

    xref_symbols: List[XRefSymbol]
    """
    All associated cross-reference symbols for this asset.
    """


class AssetSearchRequest(CamelModel):
    """
    Request for performing a structured query of the asset database.
    The system may apply limits on the size of the response if the
    scope of the query is too large. Note at this time this query
    is always applied against the latest version of the asset master.

    Wildcards here should be interpreted to maximize matches rather
    than being treated as exclusive AND conditions, i.e. if the
    user requests TOKEN and OPTION assets and specifies an expiry
    date as well, this should be used to limit the OPTION but still
    return any matching TOKEN assets.

    At this time you cannot filter to PUT or CALL options only
    or limit by option style, e.g. EUROPEAN, or contract size;
    the full option chain will be returned, with any expiry
    and strike filters applied.
    """

    asset_types: Optional[List[AssetType]]
    """
    Asset types to query, or all if not specified or empty.
    """

    exchange_ids: Optional[List[UUID]]
    """
    For listed derivatives, the exchanges to include.
    """

    underlier_assets: Optional[List[UUID]]
    """
    For derivatives, the underliers. For spot, the token asset or,
    for wrapped assets or stableassets, the underlying asset.
    """

    expiries: Optional[List[date]]
    """
    For futures and options, the expiries to include.
    """

    strikes: Optional[List[float]]
    """
    For options only, the strike prices to include.
    """

    include_expired: bool = False
    """
    Whether to include expired contracts. In the first release
    this will ALWAYS be False to limit search space, and the
    backend will reject; parameter included for documentation
    purposes only at this time.
    """

    offset: Optional[int]
    """
    The number of records to skip in the page.
    """

    limit: Optional[int] = Field(1000, le=1000)
    """
    The maximum number of items that should be returned.
    Cannot exceed more than 1000 records.
    """

    @validator('include_expired', always=False)
    def check_include_expired_vs_expiries(cls, include_expired, values):
        if (not include_expired) and values.get('expiries'):
            if any([e < date.today() for e in values.get('expiries')]):
                raise ValueError(
                    "Some of the expiry dates have already expired and include_expired is set to False")
        return include_expired
