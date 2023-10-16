from datetime import datetime
from enum import Enum
from typing import Dict, List, Union
from uuid import UUID
from pydantic import Field

from serenity_types.utils.serialization import CamelModel
from serenity_types.pricing.core import AsOfTimeRange, EffectiveDateTime


class VolModel(Enum):
    """
    Currently supported volatility models.
    """

    SVI = "SVI"
    """
    Stochastic volatility (SVI) calibrated volatility model.
    """

    BLACK_SCHOLES = "BLACK_SCHOLES"
    """
    Classic Black-Scholes volatility model.
    """


class StrikeType(Enum):
    """
    Currently supported strike representations.
    """

    ABSOLUTE = "ABSOLUTE"
    """
    Absolute value of strike, e.g. the 20000 option.
    """

    LOG_MONEYNESS = "LOG_MONEYNESS"
    """
    Relative value of strike vs. current spot with log transformation: log(strike / spot).
    """


class DiscountingMethod(Enum):
    """
    The strategy to use for deriving the discount rate, i.e. the assumed interest rate to
    use when discounting prices to present.
    """

    CURVE = "CURVE"
    """
    Extract a discount factor from discount curves, either provided via API or loaded from database.
    """

    SELF_DISCOUNTING = "SELF_DISCOUNTING"
    """
    Use the base asset's projection rate as the discount rate instead of a discount curve.
    This is the default, and the option you should choose if you want to reproduce the Deribit
    forward pricing model.
    """


class ProjectionMethod(Enum):
    """
    The strategy to use for deriving the projection rates, i.e. the forward interest rates.
    """

    CURVE = "CURVE"
    """
    Projection rate is extracted from a projection curve, either provided via API or loaded from database.
    This option is respected in both real-time pricing and historical pricing modes, though in real-time
    the curve version loaded is always the very latest. Select CURVE if you want a more stable forward.
    """

    FUTURES = "FUTURES"
    """
    Projection rate is snapped from the corresponding Deribit futures prices; this option is only
    supported in real-time pricing mode. Select FUTURES if in real-time you want to reproduce
    Deribit forward pricing model and incorporate up-to-the-moment market view on the forward.
    """


class VolatilitySurfaceDefinition(CamelModel):
    """
    A uniquely-identified set of VS parameters for fitting a VolatilitySurface.
    """

    vol_surface_id: UUID
    """
    Unique ID for this volatility surface's collection of attributes; note that surfaces
    are re-fitted hourly, and so there are going to be many versions over time.
    """

    vol_model: VolModel
    """
    Volatility model used for this surface.
    """

    strike_type: StrikeType
    """
    Strike representation used for this surface, e.g. ABSOLUTE or LOG_MONEYNESS.
    """

    underlier_asset_id: UUID
    """
    The linked asset for this surface, e.g. for a Bitcoin volatility surface, this is BTC (tok.btc.bitcoin).
    Note we will be switching to the Exposure UUID instead in a future release (e.g. tok.btc), once the
    reference data is available.
    """

    display_name: str
    """
    Human-readable description of this curve, e.g. Deribit BTC (SVI, ABSOLUTE)
    """


class VolatilitySurfaceAvailability(CamelModel):
    """
    Information about version availability for a given volsurface definition.
    """

    definition: VolatilitySurfaceDefinition
    """
    Description of the particular volsurface parameters that are available to load.
    """

    as_of_times: List[datetime] = Field(
        deprecated=True,
        description="(DEPRECATED) Refer to effective_times instead of this"
    )
    """
    The list of all available as_of_times in the requested window.
    """

    effective_times: List[EffectiveDateTime]
    """
    The list of all available EffectiveDateTime in the requested window.
    """


class VolPoint(CamelModel):
    """
    An individual IV input point.
    """

    option_asset_id: UUID
    """
    The specific option that was used for vol fitting purposes.
    """

    time_to_expiry: float
    """
    The time to expiry for this point, expressed as a year fraction.
    """

    strike_value: float
    """
    Value of strike for this point, unit defined by StrikeType.
    """

    mark_price: float
    """
    The observed option premium used as input to the IV calculation.
    """

    projection_rate: float
    """
    The projection rate used when computing the forward.
    """

    discounting_rate: float
    """
    The discounting rate used when computing the forward; equal to projection_rate with SELF_DISCOUNTING,
    which is currently the default for our IV calculations.
    """

    forward_price: float
    """
    The computed forward price that went into the IV calculation.
    """

    iv: float
    """
    The computed implied volatility (IV) that corresponds to the given mark_price and other inputs.
    """


class RawVolatilitySurface(CamelModel):
    strike_type: StrikeType
    """
    Strike representation used for this surface, e.g. ABSOLUTE or LOG_MONEYNESS.
    """

    spot_price: float
    """
    The observed spot price that went into the IV calculations.
    """

    vol_points: List[VolPoint]
    """
    The discrete IV points available for fitting as a volatility surface.
    """


class InterpolatedVolatilitySurface(CamelModel):
    """
    A calibrated volatility surface with a dense grid of fitted vols. Each array
    is of equal length and corresponds to (x, y, z) for the mesh.
    """

    definition: VolatilitySurfaceDefinition
    """
    The unique set of parameters used to calibrate / fit this surface.
    """

    strikes: List[float]
    """
    All strikes expressed as log-money values, the x-axis in the mesh.
    """

    time_to_expiries: List[float]
    """
    All times to expiry expressed as year fractions, the y-axis in the mesh.
    """

    vols: List[float]
    """
    All fitted vols, the z-axis in the mesh.
    """

    input_params: Dict[str, object]
    """
    Informational set of input parameters, e.g. yield curves used for the forward. May be empty
    and keys will depend on the configuration, e.g. DiscountingType.
    """

    calibration_params: Dict[float, Dict[str, float]]
    """
    Informational set of calibration parameters, e.g. the SVI parameters. Keying is time_to_expiry
    expressed in year fractions to parameter set, where the parameter keys are VolModel-specific.
    """


class VolatilitySurfaceVersionRequest(CamelModel):
    """
    A request for one or more versions of a specific volatility surface. Used for plotting
    on the front-end to show how the surface evolves over a narrow time window.
    """

    vol_surface_id: UUID
    """
    The specific combination of parameters (VolModel, etc.) that you want to retrieve from the database.
    """

    as_of_times: Union[AsOfTimeRange, List[datetime]]
    """
    Either a start/end range of as-of times for VolatilitySurfaceVersions to retrieve, or an explicit
    list of as-of times to load. The combination of UUID + as-of times gives you a list of
    VolatilitySurfaceVersions to retrieve.
    """


class VolatilitySurfaceVersion(CamelModel):
    """
    A single version of a fitted volatility surface, with both the raw and interpolated content.
    """

    raw: RawVolatilitySurface
    """
    The raw volatility surface inputs.
    """

    interpolated: InterpolatedVolatilitySurface
    """
    The interpolated volatility surface.
    """

    as_of_time: datetime = Field(
        deprecated=True,
        description="(DEPRECATED) Refer to effective_time instead of this"
    )
    """
    The time window, generally top of the hour, for which we have fitted the volatility surface; latest prices
    as of this time are used as input to the surface calibration.
    """

    effective_time: EffectiveDateTime
    """
    The effective time range, for which we have fitted the volatility surface; latest prices
    as of this time are used as input to the surface calibration.
    """

    build_time: datetime
    """
    The actual time of the build; due to DQ or system issues this might be different from as_of_time.
    """


class Axis(Enum):
    """
    Enumeration of the X, Y axes for the surface.
    """

    TIME_TO_EXPIRY = 'TIME_TO_EXPIRY'
    """
    Slice range denotes start and end time to expiry as a year fraction.
    """

    STRIKE = 'STRIKE'
    """
    Slice range denotes start and end strikes according to the surface type, e.g. log moneyness or absolute strike.
    """


class PillarDate(Enum):
    """
    A standard time-to-expiry. Use for drop-downs to select slices for Axis.TIME_TO_EXPIRY.
    """

    label: str
    """
    Display label to use: 1D, 1W, 1M, 3M, 6M, 1Y.
    """

    time_to_expiry: float
    """
    Relative date expressed as a year fraction.
    """


class SliceSpecification(CamelModel):
    """
    Specification of a volatility surface "slice" -- to extract the volatility smile along either
    the expiry axis or strike axis.
    """

    axis: Axis
    """
    Axis to slice at: time-to-expiry or strike. With Axis.TIME_TO_EXPIRY, then for every
    strike on the surface you'll get a 2D array of strike, IV. With Axis.STRIKE, then
    for every time to expiry on the surface you'll get a 2D array of time_to_expiry, IV.
    """

    value: float
    """
    The X or Y value to position the slice on the surface.
    """


class SliceRequest(CamelModel):
    """
    A request to load one or more volatility surfaces and take one or more "cuts" of the surface.
    This lets the front-end efficiently batch requests to get all data required for a multi-time
    plot of how the volatility smile evolves through time.
    """

    surfaces: VolatilitySurfaceVersionRequest
    """
    A specification of which volatility surfaces to load and slice.
    """

    slices: List[SliceSpecification]
    """
    Specification of where to slice the volatility surface version(s)., e.g. show the volatility smile
    at the time_to_expiry values corresponding to 1M, 3M and 6M pillar dates.
    """


class Slice(CamelModel):
    """
    A slice from a 3D volatility surface to show the volatility smile at a particular time-to-expiry or strike.
    """

    vol_surface_id: UUID
    """
    The specific combination of parameters (VolModel, etc.) retrieved from the database.
    """

    as_of_time: datetime
    """
    As-of time for the particular volatility surface version that was sliced.
    """

    specification: SliceSpecification
    """
    Associated specification for this slice: where the slice was made.
    """

    values: List[float]
    """
    List of times to expiry or strikes, depending on SliceSpecification.
    """

    vols: List[float]
    """
    List of corresponding IV values for the given times or strikes.
    """
