"""
Helper functions for rendering asset search results
"""
from enum import Enum
from typing import List, Optional
import pandas as pd


def make_option_grid_df(option_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a grid of options from a dataframe of options
    """
    option_df['CP'] = option_df['option_type'].apply(lambda x: x.value[0])
    option_df['EX'] = option_df['expiry_datetime'].apply(lambda x: x.strftime('%d%b%y').upper())
    option_df['K'] = option_df['strike_price'].apply(lambda x: int(x))
    grid_df = option_df.groupby(['expiry_datetime', 'EX', 'K', 'CP'])[
        'native_symbol'].count().unstack([0, 1, 3]).fillna(0)
    grid_df.columns = grid_df.columns.droplevel(0)
    for c in grid_df.columns:
        grid_df[c] = grid_df[c].apply(lambda x: 'o' if x > 0 else '')
    grid_df.columns.names = [None for _ in grid_df.columns.names]
    grid_df.index.names = [None for _ in grid_df.index.names]
    return grid_df


def make_asset_symbol_df(asset_df: pd.DataFrame, order_by_cols: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Create a table of asset symbols from a list of assets
    """
    if order_by_cols is None:
        # by default, sort by `symbol` as it is an internally homogenized representation of the asset
        order_by_cols = ['symbol']

    for col in asset_df.columns:
        if isinstance(asset_df[col].iat[0], Enum):
            asset_df[col] = asset_df[col].apply(lambda x: x.value)

    return asset_df.sort_values(by=order_by_cols).set_index('native_symbol')
