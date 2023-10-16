"""
Serializables needed for the computation of the distribution measures.
"""

from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Union
from uuid import UUID
from datetime import datetime

from pydantic import Field, validator
from serenity_types.utils.serialization import CamelModel
from serenity_types.portfolio.core import AssetPosition
from serenity_types.refdata.options import OptionType, OptionStyle
from serenity_types.refdata.derivatives import SettlementType


class MeasureType(Enum):
    """
    Enum for the risk measure type.
    """

    VAR = "VaR"
    "The standard Value at Risk, i.e. the expected loss at the given confidence level."
    GAR = "GaR"
    "The Gain at Risk, i.e. the expected gain at the given confidence level."
    CVAR = "CVaR"
    "The Conditional Value at Risk, i.e. the expected loss given that the loss is greater than the VaR."
    CGAR = "CGaR"
    "The Conditional Gain at Risk, i.e. the expected gain given that the gain is greater than the GaR."
    KVAR = "KVaR"
    "The (biased) Kernel Value at Risk, i.e. the expected loss around the given confidence level."
    KGAR = "KGaR"
    "The (biased) Kernel Gain at Risk, i.e. the expected gain around the given confidence level."
    STDEV = "StDev"
    "The standard deviation of the distribution."
    UPDEV = "UpsideDev"
    "The gains standard deviation."
    DOWNDEV = "DownsideDev"
    "The losses standard deviation."


class MeasureParameters(CamelModel):
    "Parameters for a single risk measure."
    measure_type: MeasureType
    "The risk measure type chosen from the list of risk measure types."
    tag: str = ""
    "The tag of the risk measure, unique within the list of risk measures."
    confidence_level: Optional[Decimal] = Field(None, gt=0.5, lt=1.0)
    """The confidence level value. Needed for distortion measures such as VaR and CVaR. Not needed for volatility.

    Note: using "confidence_level" as the parameter name makes it clear that you are looking for the value below which
    a certain percentage of the distribution lies, rather than simply a specific percentile or quantile.
    """


class RiskComputationRequest(CamelModel):
    """
    Configuration for the risk measures.

    :param lookback_days: The lookback period expressed in days.

    ## Notes on the parameters

    ### The lookback days parameter

    The term "lookback_days" refers to the time period over which historical data is considered when computing risk.
    It represents the number of days in the past that are taken into account for analyzing and calculating risk.
    In risk analysis, historical data is often used to assess the probability and potential impact of future events
    or outcomes. By examining past data, patterns, and trends, you can gain insights into the potential risks
    associated with a particular system, investment, or activity.
    The "lookback_days" parameter allows you to specify how far back in time you want to analyze historical data
    when calculating risk. For example, if you set "lookback_days" to 360, it means you are considering the data
    from the past year for risk assessment.
    The appropriate value for "lookback_days" depends on the specific context and requirements of your risk
    calculation, however setting the "lookback_days" parameter to 360 is a good starting point for in most cases.

    ### The sampling hours parameter

    The term "sampling_hours" typically refers to the time interval between each sample when computing risk. It
    represents the duration for which data is collected or observed to analyze and calculate risk. For example,
    in the context of your hourly samples, the "sampling_hours" would be 1 hour since you are collecting data on an
    hourly basis. Each sample represents a data point collected at a specific hour, and the "sampling_hours"
    indicates the time span between consecutive samples. If daily samples are collected, then the "sampling_hours"
    would be 24 hours. Each sample represents a data point collected. In order to increase the accuracy of your
    distribution, the advice is to keep the "sampling_hours" as low as possible. The "sampling_hours" value  of 1
    hour is a good starting point for most cases. In case that daily scenarios are needed, the advice is to still
    keep the "sampling_hours" as 1 and to set the "horizon_scale" to 24.

    ### The horizon scale parameter

    The term "horizon_scale" refers to the time period or duration over which the risk is projected. It represents
    the length of time, in "sampling_hours", for which the risk assessment is made.
    The "horizon_scale" parameter allows you to specify the desired time horizon for risk analysis. It determines
    the timeframe within which the risks and their associated probabilities and impacts are evaluated. The choice
    of "horizon_scale" depends on the specific requirements and objectives of the risk assessment. When the
    "sampling_hours" is set to 1, the "horizon_scale" is expressed in hours. For example, if you set "horizon_scale"
    to 24 hours, it means that the risk analysis will project or estimate the potential risks and their magnitudes
    over a 24-hour timeframe, i.e. of one day.
    While, in theory, the "horizon_scale" can be set to any value, it is recommended to keep it as low as possible
    and not to exceed the 48 hours. The reason for this is that the accuracy of the risk assessment decreases as the
    "horizon_scale" increases. This is because the risk assessment is based on historical data, and the further
    back in time you go, the less relevant the data becomes.

    ### The measures parameter

    The term "measures" refers to the list of risk measures parameters. It represents the list of distribution
    measures that are computed for the given portfolio. The list of possible distribution measures is specified in
    the "MeasureType" enumeration. Note that the concentracion measures require the "confidence_level" parameter,
    while the dispersion measures do not.
    When the measure parameter is empty in the request, a list of reasonable default measures is used. The default
    measures are: StDev, VaR, CVaR, GaR, and CGar with a confidence level of 99%.
    Also note that when the "measures" list contains duplicate tags, only the first occurrence of the tag is used.
    """

    lookback_days: int = Field(365, description="The lookback period expressed in days", ge=1)
    "The lookback period expressed in days."
    sampling_hours: int = Field(1, description="The number of hours between samples", ge=1)
    "The number of hours between samples."
    horizon_scale: Decimal = Field(
        Decimal(1.0),
        description="The length of time in sampling hours for which the risk assessment is made",
        ge=1.0,
    )
    "The length of time in sampling hours for which the risk assessment is made."
    measures: Optional[List[MeasureParameters]] = Field(None, description="The list of risk measures parameters")
    "The list of risk measures parameters"

# API Inputs


class OTCAssetTypes(Enum):
    """
    Enum for the OTC asset types.
    """

    OPTION_VANILLA = "OPTION_VANILLA"
    """
    OTC Option vanilla asset type.
    """


class OTCOptionVanillaBookingDetails(CamelModel):
    """
    OTC option vanilla booking details.
    """

    option_type: OptionType
    """
    Whether this is a put or call contract.
    """

    option_style: OptionStyle = OptionStyle.EUROPEAN
    """
    Exercise type for this option, e.g. European exercise.
    """

    strike_price: float
    """
    Strike price for the option contract, e.g. 20000.
    """

    expiry_datetime: datetime
    """
    Expiration datetime for this option.
    """

    underlier_asset_id: UUID
    """
    The underlier asset_id for this derivative contract, e.g. BTC (78e2e8e2-419d-4515-9b6a-3d5ff1448e89).
    """

    quote_asset_id: UUID
    """
    The quote asset_id for this derivative contract, e.g. USD (a9bc74b3-c761-4446-b4f2-725ae1dcf4fc).
    """

    contract_size: float
    """
    Size of the contract in qty of underlying.
    """

    settlement_asset_id: UUID
    """
    The asset that this derivatives settles in, e.g. on Deribit, CASH settled, it might be USD.
    Note we will be switching to the Exposure UUID instead in a future release.
    """

    settlement_type: SettlementType
    """
    Whether this contract settles in cash or in the underlying itself.
    """


class OTCAssetPosition(CamelModel):
    """
    A simple representation of holding a certain amount of a given OTC asset.
    """

    otc_asset_id: str
    """
    User specified unique identifier of the OTC asset.
    """

    quantity: float
    """
    The number of OTC asset held in this position.
    If positive this indicates a long position; if negative, a short one.
    """

    otc_asset_type: Optional[OTCAssetTypes] = OTCAssetTypes.OPTION_VANILLA
    """
    The OTC asset type. Currently only support OTC option vanilla.
    """

    booking_details: OTCOptionVanillaBookingDetails
    """
    Specify the OTC asset booking details.
    """


class RichRiskMeasuresRequest(CamelModel):
    portfolio: List[Union[AssetPosition, OTCAssetPosition]]
    risk_computation_request: RiskComputationRequest
    as_of_time: Optional[datetime] = None

    @validator("portfolio")
    def validate_portfolio(cls, values):
        unique_assets = {}
        unique_otc_assets = {}
        for ap in values:
            # merge duplicated asset_id
            if isinstance(ap, AssetPosition):
                current_asset = unique_assets.get(ap.asset_id)
                current_qty = current_asset.quantity if current_asset else 0
                unique_assets[ap.asset_id] = AssetPosition(asset_id=ap.asset_id, quantity=ap.quantity + current_qty)
            # raise exception for duplicated otc_asset_id
            else:
                if unique_otc_assets.get(ap.otc_asset_id) is not None:
                    raise ValueError("Duplicated otc_asset_id identified!")
                else:
                    unique_otc_assets[ap.otc_asset_id] = ap
        return list(unique_assets.values()) + list(unique_otc_assets.values())


# API Outputs

class AssetContribution(CamelModel):
    "The risk measure values for an asset"
    asset_id: UUID
    "The asset_id"
    values: Dict[str, float]
    """The risk measure values, or contribution values, for each risk-measure tag
    Null values are not included in the response.
    """


class OTCAssetContribution(CamelModel):
    "The risk measure values for an OTC asset"
    otc_asset_id: str
    "User specified unique identifier of the OTC asset."
    otc_asset_type: OTCAssetTypes
    "Serenity classification of assets"
    values: Dict[str, float]
    """The risk measure values, or contribution values, for each risk-measure tag
    Null values are not included in the response.
    """


class PortfolioRiskMeasuresValue(CamelModel):
    "The portfolio values, pv, and risk ratio"
    values: Dict[str, float]
    """The portfolio risk measure values, or contribution values.
    Null values are not included in the response.
    """
    pv: Optional[float]
    "The portfolio present value. Set to None for null responses."
    risk_ratio: Optional[Dict[str, float]]
    "The ratio between the portfolio risk measures and the portfolio present value"


class PortfolioRiskResponse(CamelModel):
    """
    Results for the risk measures.
    """
    as_of_datetime: Optional[str]
    "The latest date time of the reference data used to compute the risk scenarios"
    request: RiskComputationRequest
    "The request that generated the response"
    portfolio: PortfolioRiskMeasuresValue
    "The portfolio pv, values, and risk ratio."
    contributions: List[Union[AssetContribution, OTCAssetContribution]]
    "The contributions to the portfolio risk measures by each component asset"
    pnl_risk_scenarios: List[float]
    "The list of portfolio P&L risk scenarios"
