from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import Field, validator

import pytz

from serenity_types.utils.serialization import CamelModel


class CashTreatment(Enum):
    """
    For purposes of cash positions, what counts as cash?
    """
    FIAT_ONLY = 'FIAT_ONLY'
    """
    Include only traditional currencies, e.g. USD or EUR.
    """

    FIAT_PEGGED_STABLECOINS = 'FIAT_PEGGED_STABLECOINS'
    """
    Include both fiat and fiat pegs, e.g. USD and USDT.
    """


class MarkTime(Enum):
    """
    For purposes of closing prices in a 24x7 market, which regional market closing should be used?
    """

    NY_EOD = 'NY_EOD'
    """
    Mark prices at 4:30PM America/New_York.
    """

    LN_EOD = 'LN_EOD'
    """
    Mark prices at 4:30PM Europe/London.
    """

    HK_EOD = 'HK_EOD'
    """
    Mark prices at 4:00PM Asia/Hong_Kong.
    """

    UTC = 'UTC'
    """
    Mark prices at UTC midnight.
    """


MARK_TIME_TZ = {
    MarkTime.NY_EOD: pytz.timezone('America/New_York'),
    MarkTime.LN_EOD: pytz.timezone('Europe/London'),
    MarkTime.HK_EOD: pytz.timezone('Asia/Hong_Kong'),
    MarkTime.UTC: pytz.utc
}


class PricingContext(CamelModel):
    """
    Standard settings to use when doing pricing for risk calculation purposes,
    portfolio valuation, etc.. Generally controls which prices to select and
    how to convert those prices into the organization's base currency.
    """

    as_of_date: Optional[date] = Field(
        deprecated=True,
        description="(DEPRECATED) Use as_of_time instead of this"
    )
    """
    The date on which the portfolio was valued; default to latest date.
    """

    as_of_time: Optional[datetime] = None
    """
    The datetime on which the portfolio was valued; default to latest datetime.
    """

    mark_time: Optional[MarkTime] = MarkTime.UTC
    """
    The close time convention to use for close-on-close prices in the 24x7 market.
    """

    base_currency_id: Optional[UUID] = None
    """
    The accounting currency to use for valuation, reporting, etc., e.g. fund reports in USD.
    """

    cash_treatment: Optional[CashTreatment] = CashTreatment.FIAT_ONLY
    """
    What to consider to be a cash position, e.g. for NAV calcs.
    """

    # this is to handle deprecating as_of_date field
    @validator('as_of_time', always=True)
    def set_as_of_time_from_as_of_date(cls, as_of_time, values):
        if as_of_time is None and values.get('as_of_date'):
            return datetime.combine(values.get('as_of_date'), datetime.min.time())
        return as_of_time


class AsOfTimeRange(CamelModel):
    """
    Simple helper object that specifies a datetime range as a single object.
    """

    start_time: datetime
    """
    Start of the range, inclusive.
    """

    end_time: datetime
    """
    End of the range, inclusive.
    """


class EffectiveDateTime(CamelModel):
    """
    The effective datetime range of the returned batch data. None denotes realtime data.
    """

    as_of_from_ts: datetime
    """
    Start of the bitemporal as-of time: when this data is effective *from*.
    """

    as_of_to_ts: datetime
    """
    End of the bitemporal as-of time: when this data is effective *to*.
    """
