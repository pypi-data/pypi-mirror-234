"""
This module contains functions that return market data for demo purposes
"""

from uuid import UUID

from serenity_sdk.api.provider import SerenityApiProvider
from serenity_types.pricing.derivatives.options.volsurface import StrikeType


def validate_pricer_supported_underlier(
        api: SerenityApiProvider,
        underlier_id: UUID) -> None:
    """
    Validate that the underlier is supported by the API
    """

    supported_underliers = [underlier.asset_id for underlier in api.pricer().get_supported_underliers()]
    if underlier_id not in supported_underliers:
        raise ValueError(f"{underlier_id} is not supported. Must be one of {supported_underliers}")


def get_spot_price(
    api: SerenityApiProvider,
    underlier_id: UUID
):
    """
    Get the spot price for a given underlier asset using the pricer API
    """
    validate_pricer_supported_underlier(api, underlier_id)

    versions = api.pricer().get_available_volatility_surface_versions()

    vol_surf_version = [v for v in versions if v.definition.underlier_asset_id ==
                        underlier_id and v.definition.strike_type == StrikeType.LOG_MONEYNESS][0]

    vs_obj = api.pricer().get_volatility_surface_version(vol_surf_version.definition.vol_surface_id)

    return vs_obj.raw.spot_price
