
from typing import List
import pandas as pd
from serenity_types.utils.serialization import CamelModel


def make_df_from_list(obj_list: List[CamelModel]) -> pd.DataFrame:
    """
    Create a dataframe from a list of camel models
    """
    return pd.DataFrame(a.dict() for a in obj_list)
