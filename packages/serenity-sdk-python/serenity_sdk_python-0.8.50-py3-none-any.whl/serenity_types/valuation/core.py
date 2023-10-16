from typing import Dict, List, Optional, Union
from pydantic import validator, root_validator
from math import isnan
from uuid import UUID
from datetime import datetime, timezone
from enum import Enum
from typing_extensions import Annotated

from serenity_types.portfolio.core import AssetPosition
from serenity_types.pricing.core import PricingContext
from serenity_types.utils.serialization import CamelModel

NumberOrNanReplacement = Annotated[Union[float, str], ""]


class PositionValue(CamelModel):
    """
    Value of a single position in the portfolio.
    """

    value: float
    """
    The value of this position in base currency, e.g. qty * price for simple asset types.
    """

    price: float
    """
    The price for this position according to the chosen mark time.
    """

    qty: float
    """
    The quantity of assets, e.g. 0.7 BTC.
    """

    weight: float
    """
    The weight of this position in the overall portfolio, as a fraction, e.g. 0.12.
    This is just the position's value divided by the portfolio value.
    """

    @root_validator
    def convert_nan_to_zero_position_value(cls, values):
        for field in values.keys():
            field_value = values[field]
            values[field] = (
                0 if (field_value is None or isnan(field_value)) else field_value
            )
        return values


class PositionValuation(CamelModel):
    """
    Close, previous and current values of a single position in the portfolio.
    """

    close: PositionValue
    """
    The value of the asset at the MarkTime, as of the most recent close.
    """

    previous: PositionValue
    """
    The value of the asset at the MarkTime, as of the previous close.
    """

    current: Optional[PositionValue]
    """
    The value of the position as of the current moment. Requires real-time
    data that will be connected in Q1'23.
    """


class PortfolioValue(CamelModel):
    """
    Total value of the portfolio as of a certain time.
    """

    net_holdings_value: float
    """
    The sum of the values of all non-cash positions.
    """

    gross_holdings_value: float
    """
    The sum of the absolute values of all non-cash positions.
    """

    cash_position_value: float
    """
    The fiat position or stablecoin equivalent based on settings determining whether stablecoins count as cash.
    """

    net_asset_value: float
    """
    NAV, i.e. net_position_value + cash_position_value.
    """

    @root_validator
    def convert_nan_to_zero_portfolio_value(cls, values):
        for field in values.keys():
            field_value = values[field]
            values[field] = (
                0 if (field_value is None or isnan(field_value)) else field_value
            )
        return values


class PortfolioValuationRequest(CamelModel):
    """
    Request to do a NAV calculation for a portfolio. This is simple right now,
    but once we support non-linear assets we will need to extend it.
    """

    portfolio: List[AssetPosition]
    """
    Basic, moment-in time image of the portfolio to be valued.
    """

    pricing_context: PricingContext
    """
    Common settings related to how to value the portfolio, e.g. which prices to load.
    """

    @validator("portfolio")
    def merge_duplicated_asset_positions(cls, values):
        unique_assets = {}
        for ap in values:
            current_asset = unique_assets.get(ap.asset_id)
            current_qty = current_asset.quantity if current_asset else 0
            unique_assets[ap.asset_id] = AssetPosition(
                asset_id=ap.asset_id, quantity=ap.quantity + current_qty
            )
        return list(unique_assets.values())


class PortfolioValuationResponse(CamelModel):
    """
    Response with the value of the portfolio at top level plus all position values.
    """

    pricing_context: PricingContext
    """
    The context that was used to value this portfolio. DEPRECATED, not needed.
    """

    close: PortfolioValue
    """
    The value of the whole portfolio as of the most recent close date.
    """

    previous: PortfolioValue
    """
    The value of the whole portfolio as of the previous close date.
    """

    current: Optional[PortfolioValue]
    """
    The value of the whole portfolio as of real-time price.
    """

    positions: Dict[str, PositionValuation]
    """
    The values of each of the individual positions in the portfolio keyed by asset UUID.
    """


class NetDeltaConversionRequest(CamelModel):
    """
    Request to do net delta equivalent conversion for a given portfolio.
    """

    portfolio: List[AssetPosition]
    """
    Basic, moment-in time image of the portfolio to be valued.
    """

    pricing_context: Optional[PricingContext]
    """
    Common settings related to how to value the portfolio, e.g. which prices to load.
    """

    @validator("portfolio")
    def merge_duplicated_asset_positions(cls, values):
        unique_assets = {}
        for ap in values:
            current_asset = unique_assets.get(ap.asset_id)
            current_qty = current_asset.quantity if current_asset else 0
            unique_assets[ap.asset_id] = AssetPosition(
                asset_id=ap.asset_id, quantity=ap.quantity + current_qty
            )
        return list(unique_assets.values())

    # TODO: Additional overides


class CompoundingFrequency(Enum):
    """
    Compounding frequency inputs for returns data
    """

    HOURLY = 24 * 365
    DAILY = 365
    WEEKLY = 52
    MONTHLY = 12
    YEARLY = 1


class CompoundingFrequencyInput(Enum):
    """
    Compounding frequency inputs for returns data
    """

    HOURLY = 'HOURLY'
    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    MONTHLY = 'MONTHLY'
    YEARLY = 'YEARLY'


class ReturnsType(Enum):
    """
    Calculation treatment for portfolio returns
    """

    SIMPLE = "SIMPLE"
    """
    Use simple percentage returns.
    """

    LOG = "LOG"
    """
    Use logarithmic returns
    """


class RebalancingFrequency(Enum):
    """
    How often the porfolio rebalances to given weight.
    """

    DAILY = "DAILY"
    """
    Perform a daily rebalance at the closing time based on MarkTime.
    """


class PortfolioTimeseriesFrequency(Enum):
    """
    When creating a portfolio from weights or trades and transfers,
    how frequently to generate snapshots with position balances.
    """

    HOURLY = "HOURLY"
    """
    Compute position balances at the end of each hourly period.
    """

    DAILY = "DAILY"
    """
    Compute position balances at the end of each day at a daily close based on MarkTime.
    """

    MONTHLY = "MONTHLY"
    """
    Compute position balances at the end of each month at a daily close based on MarkTime.
    """


class AssetWeight(CamelModel):
    """
    Tuple representing a single position represented as an asset
    and a percentage weight: an allocation.
    """

    asset_id: UUID
    """
    Unique ID for the asset from the Serenity asset master.
    """

    weight: float
    """
    Allocated weight for this asset, expressed as a fraction.
    """


class PositionTimeseries(CamelModel):
    """
    Historical time series of position balances, expressed as quantities.
    """

    as_of_time: List[datetime]
    """
    Series of timestamps for the positions.
    """

    asset_id: List[UUID]
    """
    Series of unique asset identifiers from the Serenity asset master.
    """

    quantity: List[List[float]]
    """
    Matrix of quantities for each as_of_time, asset_id pair.
    """

    @validator("as_of_time")
    def check_as_of_time_include_tz(cls, as_of_time):
        return [
            t.replace(tzinfo=timezone.utc) if t.tzinfo is None else t
            for t in as_of_time
        ]


class TradeCommission(CamelModel):
    """
    A trade commission expressed as an asset rather than USD.
    """

    asset_id: UUID
    """
    Unique ID for the asset from the Serenity asset master.
    """

    quantity: float
    """
    Quantity of the asset paid as commission.
    """


class Trades(CamelModel):
    """
    A set of trades applied to a portfolio. All lists are understood in parallel,
    so index 0 is the first fill in the series, with timestamps, asset ID's, etc.
    as separate series.
    """

    trade_datetime: List[datetime]
    """
    Series of exact timestamps of the trade / fill.
    """

    base_asset_id: List[UUID]
    """
    Series of unique asset ID's of the traded instruments, e.g. in BTC-USD, BTC.
    """

    quote_asset_id: List[UUID]
    """
    Series of unique asset ID's of the quote instruments used to fund the trades,
    e.g. in BTC-USD, USD.
    """

    quantity: List[float]
    """
    Series of fill quantities for the trades.
    """

    fill_price: List[float]
    """
    Series of fill prices for the trades, expressed in quote asset.
    """

    commission_in_usd: List[float]
    """
    Series of commissions paid for the trades, expressed in USD for convenience.
    In a future release this will be generalized to use TradeCommission, allowing
    expression of fees in any asset.
    """

    @validator("trade_datetime")
    def check_trade_datetime_include_tz(cls, trade_datetime):
        return [
            t.replace(tzinfo=timezone.utc) if t.tzinfo is None else t
            for t in trade_datetime
        ]

    @root_validator
    def check_all_fields_equal_len(cls, values):
        fields_length = [len(v) for _, v in values.items()]
        if len(set(fields_length)) != 1:
            raise ValueError("All Trades fields need to be in the same length")
        return values


class Transfers(CamelModel):
    """
    A set of transaction moving assets from one account -- typically external --
    in or out of an exchange account.
    """

    transfer_datetime: List[datetime]
    """
    Series of exact timestamps of the transfers executed.
    """

    asset_id: List[UUID]
    """
    Series of unique asset ID's transferred in or out of the account.
    """

    quantity: List[float]
    """
    Series of transfer amounts.
    """

    @validator("transfer_datetime")
    def check_transfer_datetime_include_tz(cls, transfer_datetime):
        return [
            t.replace(tzinfo=timezone.utc) if t.tzinfo is None else t
            for t in transfer_datetime
        ]

    @root_validator
    def check_all_fields_equal_len(cls, values):
        fields_length = [len(v) for _, v in values.items()]
        if len(set(fields_length)) != 1:
            raise ValueError("All Transfers fields need to be in the same length")
        return values


class PortfolioTimeseriesAndTrades(CamelModel):
    """
    Portfolio quantity timeseries, trades, and transfers.
    """

    positions: PositionTimeseries
    """
    Series of portfolio quantities of Serenity supported assets.
    """

    trades: Optional[Trades] = None
    """
    Trades associated with this portfolio.
    """

    transfers: Optional[Transfers] = None
    """
    Transfers associated with this portfolio.
    """


class BasePortfolioComposition(CamelModel):
    """
    Base portfolio/benchmark composition.
    Different portfolios/benchmarks rebalance at different times, and according to their
    own rules, and this cannot be captured in simple metadata. We just capture
    the output, provided by the vendor.
    """

    as_of_time: List[datetime]
    """
    Series of timestamps of the compositions. Generally it's a date midnight,
    but for full generality expressed as a datetime.
    """

    weight: Optional[List[List[float]]] = None
    """
    Composition by specifying percentage weights, expressed as fractions for each as_of_time, asset_id pair
    Should not be used together with 'quantity'.
    """

    quantity: Optional[List[List[float]]] = None
    """
    Composition by specifying quantity for each as_of_time, asset_id pair
    Should not be used together with 'weight'.
    """

    @validator("as_of_time")
    def check_as_of_time_include_tz(cls, as_of_time):
        return [
            t.replace(tzinfo=timezone.utc) if t.tzinfo is None else t
            for t in as_of_time
        ]

    @root_validator
    def check_quantity_and_weight(cls, values):
        if (values.get('quantity') is None and values.get('weight') is None) or \
                (values.get('quantity') and values.get('empty')):
            raise ValueError("Only one of 'weight' or 'quantity' should be specified.")
        return values


class PortfolioComposition(BasePortfolioComposition):
    """
    Series of portfolio/benchmark weights or positions for all Serenity supported assets.
    """

    asset_id: List[UUID]
    """
    Series of unique asset identifiers from Serenity asset master.
    """

    prices: Optional[List[List[float]]] = None
    """
    Series of user specified mark prices, presumed in V1 to be USD only, which were used to calculate NAV.
    Optional field for PortfolioComposition. If not specified, use Serenity's sourced prices.
    """

    @validator("asset_id")
    def check_duplicated_asset_id(cls, asset_id):
        if len(set(asset_id)) != len(asset_id):
            raise ValueError("Identified duplicated asset_id")
        return asset_id


class CustomizedPortfolioComposition(BasePortfolioComposition):
    """
    Series of portfolio/benchmark weights or positions for all custom assets.
    """

    custom_asset_id: List[str]
    """
    Series of unique custom asset identifiers.
    This can be anything as long as each custom_asset_id is unique.
    """

    prices: List[List[float]]
    """
    Series of user specified mark prices, presumed in V1 to be USD only, which were used to calculate NAV.
    Mandatory field for CustomizedPortfolioComposition.
    """

    @validator("custom_asset_id")
    def check_duplicated_custom_asset_id(cls, custom_asset_id):
        if len(set(custom_asset_id)) != len(custom_asset_id):
            raise ValueError("Identified duplicated custom_asset_id")
        return custom_asset_id


class PortfolioCompositionAndTrades(CamelModel):
    """
    Specify portfolio compositions, trades, and transfers.
    """

    positions: Union[PortfolioComposition, CustomizedPortfolioComposition]
    """
    Series of portfolio weights or quantities of Serenity supported assets or custom assets.
    """

    trades: Optional[Trades] = None
    """
    Trades associated with this portfolio.
    """

    transfers: Optional[Transfers] = None
    """
    Transfers associated with this portfolio.
    """
