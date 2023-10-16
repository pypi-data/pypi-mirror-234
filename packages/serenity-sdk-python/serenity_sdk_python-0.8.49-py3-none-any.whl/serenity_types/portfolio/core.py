from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID
from pydantic import validator

from serenity_types.ledger.balance import Balance
from serenity_types.utils.serialization import CamelModel
from serenity_types.refdata.asset import UnsupportedAsset


class AssetPosition(CamelModel):
    """
    A simple representation of holding a certain amount of a given asset.
    This is going to be replaced with a much more flexible Portfolio
    representation in Q1'23.
    """

    asset_id: UUID
    """
    Unique identifier of the asset from Serenity's asset master database.
    """

    quantity: float
    """
    The number of tokens, shares, contracts, etc. held in this position.
    If positive this indicates a long position; if negative, a short one.
    """


class SimplePortfolio(CamelModel):
    """
    A simple portfolio representation that just maps the positions to
    positive or negative quantities for long and short. There is no
    history, detail on custody or any other context.
    """

    portfolio_id: UUID
    """
    Unique ID; in the initial implementation this is assigned locally in
    a client installation-hosted database.
    """

    base_currency_id: UUID
    """
    Asset ID of the base currency for this portfolio.
    """

    portfolio_name: str
    """
    Descriptive name for this portfolio, for display only.
    """

    portfolio_manager: str
    """
    In the initial implementation, a text field for the PM;
    eventually will link to user ID in the database.
    """

    asset_positions: List[AssetPosition]
    """
    List of positions in the portfolio.
    """

    @validator("asset_positions")
    def merge_duplicated_asset_positions(cls, values):
        unique_assets = {}
        for ap in values:
            current_asset = unique_assets.get(ap.asset_id)
            current_qty = current_asset.quantity if current_asset else 0
            unique_assets[ap.asset_id] = AssetPosition(asset_id=ap.asset_id, quantity=ap.quantity + current_qty)
        return list(unique_assets.values())


class NetDeltaPortfolioPositions(CamelModel):
    """
    Representing the 'before' and 'after' AssetPositions of a
    net-delta converted portfolio's positions.
    """

    original_asset_positions: List[AssetPosition]
    """
    The original AssetPosition specified by user - before net-delta conversion.
    """

    net_delta_asset_positions: List[AssetPosition]
    """
    The result of net-delta conversion AssetPosition.
    """


class StrategyType(Enum):
    """
    The strategy an investor follows when making investment decisions.
    """

    LONG_ONLY = "LONG_ONLY"
    """
    Long positions only.
    """

    SHORT_ONLY = "SHORT_ONLY"
    """
    Shorting positions only.
    """

    LONG_SHORT = "LONG_SHORT"
    """
    Takes both long and short positions in securities simultaneously.
    """

    INDEX = "INDEX"
    """
    An index strategy is to match the returns of the underlying index.
    """

    MARKET_NEUTRAL = "MARKET_NEUTRAL"
    """
    Aim to achieve returns that are independent of market movements.
    """

    ARBITRAGE = "ARBITRAGE"
    """
    Exploit pricing inefficiencies in the market.
    """

    EVENT_DRIVEN = "EVENT_DRIVEN"
    """
    Specific events or catalysts that are expected to have an impact on the price.
    """

    QUANT_SYSTEMATIC = "QUANT_SYSTEMATIC"
    """
    Using computer-based algorithms and mathematical models to analyze and trade in the market.
    """

    OTHER = "OTHER"
    """
    Other strategy type that is not available in the predefined list.
    """


class Strategy(CamelModel):
    """
    The general approach to investing and managing the portfolio.
    """

    strategy_type: StrategyType
    """
    The strategy an investor follows when making investment decisions.
    """

    description: Optional[str]
    """
    The description of the strategy.
    """


class PortfolioMetadata(CamelModel):
    """
    Metadata that are typically part of a portfolio
    """

    metadata_id: UUID
    """
    Unique and immutable ID.
    """

    name: str
    """
    A descriptive name for this portfolio.
    """

    owner: str
    """
    The primary owner of this portfolio.
    """

    version: int
    """
    Monotonically increasing version number.
    """

    updated_by: str
    """
    Last update user.
    """

    updated_at: datetime
    """
    Last update timestamp, in UTC.
    """

    base_currency_id: Optional[UUID]
    """
    The accounting currency to use for valuation, reporting, etc., e.g. fund reports in USD.
    Defaults to `USD` if it's not provided.
    """

    strategy: Optional[Strategy]
    """
    The general approach to investing and managing the portfolio.
    """

    account_ids: Optional[List[UUID]]
    """
    The authoritative sources for transaction information.
    """

    tags: Optional[List[str]]
    """
    Custom tags for the purpose of searching and filtering.
    """


class PortfolioSnapshot(CamelModel):
    """
    Snapshot of the positions of a portfolio at a specific point in time.
    """

    snapshot_id: UUID
    """
    Unique and immutable ID.
    """

    version: int
    """
    Monotonically increasing version number.
    """

    updated_by: str
    """
    Last update user.
    """

    updated_at: datetime
    """
    Last update timestamp, in UTC.
    """

    portfolio_metadata_id: UUID
    """
    The metadata that this portfolio snapshot is part of.
    """

    as_of_time: datetime
    """
    The specific point in time for the portfolio snapshot.
    """

    balances: List[Balance]
    """
    The positions/balances for the portfolio snapshot at a specific point in time.
    """

    unsupported_assets: Optional[List[UnsupportedAsset]]
    """
    The unsupported assets for the portfolio snapshot at a specific point in time.
    """


class PortfolioMetadataBaseRequest(CamelModel):
    """
    The portfolio metadata base request class
    """

    name: str
    """
    A descriptive name for this portfolio.
    """

    owner: str
    """
    The primary owner of this portfolio.
    """

    updated_by: str
    """
    Last update user.
    """

    base_currency_id: Optional[UUID]
    """
    The accounting currency to use for valuation, reporting, etc., e.g. fund reports in USD.
    Defaults to `USD` if it's not provided.
    """

    strategy: Optional[Strategy]
    """
    The general approach to investing and managing the portfolio.
    """

    account_ids: Optional[List[UUID]]
    """
    The authoritative sources for transaction information.
    """

    tags: Optional[List[str]]
    """
    Custom tags for the purpose of searching and filtering.
    """


class PortfolioMetadataCreateRequest(PortfolioMetadataBaseRequest):
    """
    Input for the create request
    """
    pass


class PortfolioMetadataUpdateRequest(PortfolioMetadataBaseRequest):
    """
    Input for the update request
    """
    pass


class PortfolioSnapshotBaseRequest(CamelModel):
    """
    The portfolio snapshot base request class
    """

    portfolio_metadata_id: UUID
    """
    The metadata that this portfolio snapshot is part of.
    """
    as_of_time: datetime
    """
    The specific point in time for the portfolio snapshot.
    """

    balances: List[Balance]
    """
    The positions/balances for the portfolio snapshot at a specific point in time.
    """

    unsupported_assets: Optional[List[UnsupportedAsset]]
    """
    The unsupported assets for the portfolio snapshot at a specific point in time.
    """

    updated_by: str
    """
    Last update user.
    """


class PortfolioSnapshotCreateRequest(PortfolioSnapshotBaseRequest):
    """
    Input for the create request
    """
    pass


class PortfolioSnapshotUpdateRequest(PortfolioSnapshotBaseRequest):
    """
    Input for the update request
    """
    pass
