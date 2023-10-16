from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import validator, Field, PositiveFloat, root_validator

from serenity_types.pricing.derivatives.options.volsurface import (
    InterpolatedVolatilitySurface, VolModel, DiscountingMethod, ProjectionMethod, StrikeType
)
from serenity_types.pricing.derivatives.rates.yield_curve import InterpolatedYieldCurve
from serenity_types.refdata.asset import AssetType
from serenity_types.refdata.options import OptionStyle, OptionType
from serenity_types.utils.serialization import CamelModel


class MarketDataOverride(CamelModel):
    """
    Helper type for representing replacements and bumps for market data inputs in pricing.
    """

    replacement: Optional[PositiveFloat]
    """
    Replacement value for the given market data point.
    """

    additive_bump: Optional[float]
    """
    A value (potentially negative) to add the observed value from stored or live market data.
    """

    @validator('replacement', always=True)
    def check_bump_or_replace_but_not_both(cls, replacement, values):
        if values.get('additive_bump') and replacement:
            raise ValueError("Please specify only one of 'replacement' or 'additive_bump'")
        return replacement


class YieldCurveOverride(CamelModel):
    """
    Helper for representing explicitly either override by UUID (load that YieldCurveDefinition
    from the database for the appropriate as_of_time) or by value. The client can also specify
    mutations to make to this input market data. In the case where you want to replace the
    rate entirely do not specify either yield_curve_id or yield_curve; in the case where you
    want to do a shift of the yield curve, specify either ID or curve and then an additive_bump.
    Everything null or both yield_curve_id and yield_curve specified yields validation errors.
    """

    yield_curve_id: Optional[UUID]
    """
    Optionally specifies a supported YieldCurveDefinition UUID from the database. Not every
    definition is accepted, e.g. you cannot pass in a CurveUsage.PROJECTION curve for discounting.
    """

    yield_curve: Optional[InterpolatedYieldCurve] = Field(
        deprecated=True,
        description="(DEPRECATED) Use a stored yield curve via yield_curve_id"
    )
    """
    Optionally specifies a supported yield curve bootstrapped by the client or loaded separately. Not every
    definition is accepted, e.g. you cannot pass in a CurveUsage.PROJECTION curve for discounting.
    """

    rate_override: Optional[MarketDataOverride]
    """
    Optionally modifies the input data. Note properly you should not need to both provide a yield_curve
    and modify it, but in case clients want to play back our stored yield_curve via API without
    having to mutate the curve themselves, it could make sense.
    """

    @validator('yield_curve', always=True)
    def check_yield_curve_ids_or_yield_curve(cls, yield_curve, values):
        if values.get('yield_curve_id') and yield_curve:
            raise ValueError("Please specify only one of 'yield_curve_id' or 'yield_curve'")
        return yield_curve


class AssetValuation(CamelModel):
    valuation_id: Optional[str]
    """
    Correlation ID to use for this requested valuation. If pricing based on a listed contract
    or a token asset, by convention the unique ID or symbol of that option should be used.
    """

    asset_id: Optional[UUID]
    """
    Look up all token or contract economics based on the unique ID of a specific asset.
    """

    asset_type: Optional[AssetType]
    """
    Type of asset being valued.
    For option valuation, defaults to LISTED_OPTION if based on asset ID, otherwise defaults to OTC_OPTION.
    """

    qty: Optional[float] = 1.0
    """
    Number of tokens or contracts. You will get unit notional for listed derivatives if you take
    the default number of contracts here. Positive values are long; negeative values are short.
    """

    ratio: Optional[PositiveFloat]
    """
    If pricing based on ratios, set this value to the multiplier to use for this leg.
    """

    @validator('ratio', always=False)
    def check_ratio_vs_qty(cls, ratio, values):
        if ratio and abs(values.get('qty')) != 1:
            raise ValueError('You cannot combine a non-unit qty and a leg ratio')
        return ratio


class OptionValuation(AssetValuation):
    """
    A collection of option economics and market data overrides used to describe a single option valuation
    requested from the service. This is intentionally meant to support both listed contract pricing and
    more general pricing of option economics. For market data, everything is defaulted, but the client can
    override or bump (shift) any of the inputs to get the exact pricing scenario desired.
    """

    option_valuation_id: Optional[str] = Field(
        deprecated=True,
        description="(DEPRECATED) Use valuation_id"
    )
    """
    Correlation ID to use for this requested option valuation. If pricing based on a listed contract
    with optionAssetId, by convention the unique ID or symbol of that option should be used.
    """

    option_asset_id: Optional[UUID] = Field(
        deprecated=True,
        description="(DEPRECATED) Use asset_id"
    )
    """
    Look up all option economics based on the unique ID of a specific listed option contract.
    """

    underlier_asset_id: Optional[UUID]
    """
    Serenity asset identifier of the underlier, e.g. BTC (tok.btc.bitcoin). Not required if optionAssetId provided.
    Note we will be switching to the Exposure UUID instead in a future release (e.g. tok.btc), once the reference
    data is available.
    """

    strike: Optional[PositiveFloat]
    """
    Absolute value of the strike. Not required if optionAssetId provided. In future we may wish to support different
    StrikeType representations here, but some cases (like DELTA) are potentially trickier, so not for initial version.
    """

    expiry: Optional[datetime]
    """
    Expiration expressed in absolute terms as a date/time. Not required if optionAssetId provided
    """

    option_type: Optional[OptionType]
    """
    Whether we are pricing a PUT or CALL option. Not required if optionAssetId provided.
    """

    option_style: Optional[OptionStyle] = OptionStyle.EUROPEAN
    """
    The variety of option being priced. Not required if optionAssetId provided.
    Our pricer only supports EUROPEAN at this time, so defaults accordingly.
    """

    contract_size: Optional[PositiveFloat]
    """
    For scaling purposes, the # of underlying per contract. Not required if optionAssetId provided, otherwise it's
    loaded from the contract specification in the database.
    """

    implied_vol_override: Optional[MarketDataOverride]
    """
    Replace or modify the stored volatility surface's IV for this option.
    """

    spot_price_override: Optional[MarketDataOverride]
    """
    Replace or modify the stored or observed spot price used when pricing this option.
    """

    @validator('option_valuation_id', always=True)
    def check_option_valuation_id_vs_valuation_id(cls, option_valuation_id, values):
        if option_valuation_id is None and values.get('valuation_id') is None:
            raise ValueError("Specify the mandatory parameter 'valuation_id'")
        elif option_valuation_id is not None and values.get('valuation_id') is not None:
            raise ValueError("Both 'option_valuation_id' and 'valuation_id' were specified, "
                             "please remove the deprecated parameter 'option_valuation_id'")
        return option_valuation_id

    @validator('option_asset_id', always=True)
    def check_option_asset_id_vs_asset_id(cls, option_asset_id, values):
        if option_asset_id is not None and values.get('asset_id') is not None:
            raise ValueError("Both 'option_asset_id' and 'asset_id' were specified, "
                             "please remove the deprecated parameter 'option_asset_id'")
        return option_asset_id

    @root_validator
    def check_asset_type_vs_asset_id(cls, values):
        is_listed_option = values.get('asset_id') or values.get('option_asset_id')
        default_asset_type = AssetType.LISTED_OPTION if is_listed_option else AssetType.OTC_OPTION
        asset_type = values.get('asset_type') or default_asset_type
        if asset_type == AssetType.OTC_OPTION and is_listed_option:
            raise ValueError('If pricing by economics, AssetType must be OTC_OPTION')
        values['asset_type'] = asset_type
        return values


class ValuationRequest(CamelModel):
    """
    Base class for batch requests for valuations of either a portfolio of options
    or for a multi-leg strategy.
    """

    as_of_time: Optional[datetime]
    """
    The as-of time to use for loading all marketdata, surfaces, yield curves and refdata from the database.
    Defaults to the latest up to this time.
    """

    model_config_id: Optional[UUID]
    """
    The specific derivatives analytics model configuration to load; this is used to drive defaults.
    Defaults to system's recommended config.
    """

    base_currency_id: Optional[UUID]
    """
    Base currency to use for expressing all notional values. Defaults to USD.
    """

    discounting_method: Optional[DiscountingMethod] = DiscountingMethod.SELF_DISCOUNTING
    """
    How to derive the discount rate: from the projection rate (self-discounting),
    or from pre-built discounting curves either provided in API or loaded from the system.
    Defaults to self-discounting.
    """

    projection_method: Optional[ProjectionMethod]
    """
    How to derive the projection rate when in real-time mode: from live futures prices, or from a curve.
    The default depends on as_of_time. In the case of as_of_time being None the system runs in real-time
    pricing mode and uses ProjectionMode.FUTURES. When as_of_time is provided the system runs in historical
    pricing mode and defaults to ProjectionMode.CURVE. Setting both as_of_time and ProjectionMode.FUTURES
    will yield a validation error from the API.
    """

    vol_surface_id: Optional[UUID]
    """
    The optional unique ID of the surface to load, latest version as-of the as_of_time.
    """

    vol_surface: Optional[InterpolatedVolatilitySurface] = Field(
        deprecated=True,
        description="(DEPRECATED) Use a stored surface via vol_surface_id"
    )
    """
    The optional client-provided volatility surface to use. If the client provides neither a VS ID
    nor their own volatility surface, the system will load the default for the underlying as-of the as_of_time.
    """

    discounting_curve_override: Optional[YieldCurveOverride]
    """
    Various forms of modifications to the discounting curve: choosing a variant in the database; passing
    in a complete curve by value; and/or replacing or shifting the extracted rate.
    """

    projection_curve_override: Optional[YieldCurveOverride]
    """
    Various forms of modifications to the projection curve: choosing a variant in the database; passing
    in a complete curve by value; and/or replacing or shifting the extracted rate.
    """

    vol_model: Optional[VolModel] = VolModel.SVI
    """
    The volatility model used for valuation purposes. Defaults to SVI.
    """

    strike_type: Optional[StrikeType] = StrikeType.LOG_MONEYNESS
    """
    The strike representation. Defaults to log-moneyness.
    """

    @validator('vol_surface', always=True)
    def check_vol_surface_id_or_vol_surface(cls, vol_surface, values):
        if values.get('vol_surface_id') and vol_surface:
            raise ValueError("Please specify only one of 'vol_surface_id' or 'vol_surface'")
        return vol_surface

    @validator('projection_method', always=False)
    def check_historical_mode_projection_method(cls, projection_method, values):
        if projection_method == ProjectionMethod.FUTURES and values.get('as_of_time'):
            raise ValueError(
                f"Historial pricing mode (asOfTime is not None) should not use {projection_method} projection method")
        return projection_method


class OptionValuationRequest(ValuationRequest):
    """
    A batch request to run one or more option valuations using a single model configuration and base
    set of curves and the vol surface. Reasonable defaults will be provided for any missing inputs, e.g.
    if you price a set of Deribit BTC options, the latest BTC volatility surface will be used along with
    the latest discounting curves for BTC and USD. Note that because the request only references a single
    volatility surface this means all included options must have the same underlier as the one in
    VolatilitySurfaceVersion.interpolated.definition.underlier_asset_id.
    """

    options: List[OptionValuation]
    """
    The full set of option valuations to run with the given market data inputs. The client may provide
    individual overrides or bumps for all inputs as part of each valuation object.
    """

    @validator('options', always=False)
    def check_non_empty_options_list(cls, options, values):
        if len(options) == 0:
            raise ValueError("Please provide at least one option in 'options'")
        return options


class LegValuationResult(CamelModel):
    """
    Base class with shared fields for leg-level valuations.
    """

    valuation_id: str
    """
    Correlation ID for the original LegValuation. By convention this should be a random UUID
    but it can also be a meaningful label like "Leg 1" or something similar.
    """

    pv: float
    """
    Present value (PV) a.k.a. theoretical price or theo. In the case of linear products this is just price.
    """

    notional_value: float
    """
    The base currency notional of the strategy position. For vanilla derivatives, this is based on the spot
    notional value: number of contracts (qty) X  spot_price X contract_size.
    """


class TokenLegValuationResult(LegValuationResult):
    """
    Valuation result for a token (spot) asset leg.
    """
    pass


class FutureLegValuationResult(LegValuationResult):
    """
    Valuation result for a future asset leg.
    """

    spot_price: float
    """
    Input spot price for this valuation.
    """

    spot_basis: float
    """
    Computed spot basis for this valuation.
    """


class PerpetualLegValuationResult(FutureLegValuationResult):
    """
    Valuation result for a perp (swap) asset leg.
    """

    funding_rate: float
    """
    Exchange funding rate at the time of valuation.
    """


class OptionValuationResult(LegValuationResult):
    """
    The result of a series of option valuations based on the parameters in the OptionValuationRequest.
    Note that the basic calculation is just Black-Scholes, but if you provide additional information
    regarding the position scaling it will also provide position notional and greek exposures
    in base currency to allow bucketing of greeks and NAV calculations.
    """

    option_valuation_id: str = Field(
        deprecated=True,
        description="(DEPRECATED) Use valuation_id"
    )
    """
    Correlation ID for the original OptionValuation.
    """

    vol_model: VolModel
    """
    The specific volatility model used; as SVI calibrations yield different greeks, this needs to be explicit.
    """

    iv: float
    """
    Implied volatility (IV)
    """

    spot_notional: float = Field(
        deprecated=True,
        description="(DEPRECATED) Use notional_value"
    )
    """
    The base currency notional of the position: number of contracts (qty) X  spot_price X contract_size.
    """

    spot_price: float
    """
    Input spot price for this valuation.
    """

    forward_price: float
    """
    Input forward price for this valuation.
    """

    projection_rate: float
    """
    The projection rate used when computing the forward.
    """

    discounting_rate: float
    """
    The discounting rate used when computing the forward; equal to projection_rate with SELF_DISCOUNTING.
    """

    delta: float
    """
    Greek output: delta, the option's sensitivity to spot changes.
    """

    delta_qty: float
    """
    Delta X qty X contract_size, the delta exposure expressed in qty of underlying.
    """

    delta_ccy: float
    """
    Delta X value, a.k.a. the partial derivative of position value with respect to spot,
    expressed in base currency
    """

    gamma: float
    """
    Greek output: gamma, the delta's sensitivity to spot changes.
    """

    gamma_ccy: float
    """
    Gamma X value^2, a.k.a. the second derivative of position value with respect to spot,
    expressed in base currency.
    """

    vega: float
    """
    Greek output: vega, the option's sensitivity to volatility changes.
    """

    vega_ccy: float
    """
    Partial derivative of the position value of the contract with respect to vega X 1%, expressed in base currency.
    """

    rho: float
    """
    Greek output: rho, the delta's sensitivity to interest rate changes.
    """

    rho_ccy: float
    """
    Partial derivative of the spot notional value of the contract with respect to rho X 1bp, expressed in base currency.
    """

    theta: float
    """
    Greek output: theta, the delta's sensitivity to time decay.
    """

    theta_ccy: float
    """
    Partial derivative of the spot notional value of the contract with respect to theta X 1 day,
    expressed in base currency.
    """


class StrategyValuationRequest(ValuationRequest):
    """
    The full set of leg valuations to run with the given market data inputs.
    """

    qty: Optional[int] = 1
    """
    Number of strategies. If leg ratios are provided, this will be used as a multipler,
    e.g. if you have a 10:1 combo with 10 tokens and 1 option contract and strategy-level
    qty is 3, you would value based on 30 tokens and 3 option contracts.
    """

    legs: List[OptionValuation]
    """
    A list of leg-level asset valuations.
    """

    @validator('legs', always=False)
    def check_non_empty_leg_list(cls, legs, values):
        if len(legs) == 0:
            raise ValueError("Please provide at least one leg in 'legs'")
        return legs


class StrategyValuationResult(CamelModel):
    """
    Value of a multi-leg strategy: both top-level, and per-leg.
    """

    pv: float
    """
    The sum of the present values of the strategy legs, i.e. the theoretical strategy value.
    """

    delta_qty: float
    """
    Sum of leg-level delta_qty's
    """

    delta_ccy: float
    """
    Sum of leg-level delta_ccy's
    """

    gamma_ccy: float
    """
    Sum of leg-level gamma_ccy's
    """

    vega_ccy: float
    """Sum of leg-level vega_ccy's, ignoring leg-level differences in expiries and strikes
    """

    rho_ccy: float
    """
    Sum of leg-level rho_ccy's, ignoring leg-level differences in expiries
    """

    theta_ccy: float
    """
    Sum of leg-level theta_ccy's
    """

    leg_results: List[OptionValuationResult]
    """
    Per-leg valuation results, e.g. the individual option values and greeks.
    """
