"""
This module contains classes for finding options for a given underlier and exchange.
"""
from datetime import datetime
from uuid import UUID
import pandas as pd
from serenity_sdk.api.provider import SerenityApiProvider
from serenity_sdk.renderers.derivatives.market_data import validate_pricer_supported_underlier
from serenity_sdk.renderers.shared.utils import make_df_from_list
from serenity_types.refdata.asset import AssetSearchRequest, AssetType
import math


class OptionFinder:

    def __init__(self,
                 api: SerenityApiProvider,
                 exchange_id: UUID,
                 underlier_id: UUID):
        """
        Initialize the option finder for a given underlier and exchange
        """

        validate_pricer_supported_underlier(api, underlier_id)

        self.option_df = make_df_from_list(api.refdata().search_assets(
            request=AssetSearchRequest(asset_types=[AssetType.LISTED_OPTION], underlier_assets=[underlier_id],
                                       exchange_ids=[exchange_id])))

        self.option_df['option_type'] = self.option_df['option_type'].apply(lambda x: x.value)

        self.expiry_datetimes = sorted(list(self.option_df['expiry_datetime'].unique()))
        self.strikes = sorted(list(self.option_df['strike_price'].unique()))

    def filter_options(
            self,
            expiry_datetime_min: datetime, expiry_datetime_max: datetime,
            strike_min: float, strike_max: float) -> pd.DataFrame:
        """
        A generic function to filter options
        """

        filtered_df = self.option_df[
            (self.option_df['expiry_datetime'] >= expiry_datetime_min)
            &
            (self.option_df['expiry_datetime'] <= expiry_datetime_max)
            &
            (self.option_df['strike_price'] >= strike_min)
            &
            (self.option_df['strike_price'] <= strike_max)
        ]
        return filtered_df

    def get_options_for_expiry(self, expiry_datetime: pd.Timestamp, strike_min: float = 0.0,
                               strike_max: float = math.inf
                               ) -> pd.DataFrame:
        """
        Get option strips for a given expiry
        """

        filtered_df = self.filter_options(expiry_datetime, expiry_datetime, strike_min, strike_max)
        return filtered_df.groupby(['strike_price', 'option_type'])['asset_id'].first().unstack()[['CALL', 'PUT']]

    def get_options_for_strike(self, strike: float) -> pd.DataFrame:
        """
        Get option strips for a given strike
        """

        strike_eps = 1e-6
        filtered_df = self.filter_options(
            self.expiry_datetimes[0], self.expiry_datetimes[-1], strike-strike_eps, strike+strike_eps)
        return filtered_df.groupby(
            ['expiry_datetime', 'strike_price', 'option_type'])['asset_id'].first().unstack()[['CALL', 'PUT']]
