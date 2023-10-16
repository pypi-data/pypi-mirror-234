from typing import Dict, List, Optional, Union
from pydantic import validator
from uuid import UUID
from datetime import datetime

from serenity_types.portfolio.core import AssetPosition
from serenity_types.utils.serialization import CamelModel
from serenity_types.pricing.core import MarkTime
from serenity_types.valuation.core import (
    AssetWeight, PortfolioTimeseriesFrequency, RebalancingFrequency,
    Trades, Transfers, PortfolioCompositionAndTrades,
    PortfolioComposition, CustomizedPortfolioComposition,
    CompoundingFrequencyInput, ReturnsType, NumberOrNanReplacement
)


class PortfolioFromAllocationRequest(CamelModel):
    """
    API request to create a portfolio from an initial cash position
    and a set of weights and a rebalancing rule. The server then generates
    a series of positions at a given frequency, e.g. daily, rebalancing
    periodically to bring the positions in line with the desired weights.
    This in turn generates a set of trades.
    """

    initial_weights: List[AssetWeight]
    """
    The model portfolio allocation in terms of weights. At start_datetime
    the system will buy the assets using the initial_cash_quantity and then
    periodically accordingly to rebalance_frequency will generate buys and
    sells to bring the allocation back in line with the initial weights.
    """

    initial_cash_quantity: float
    """
    Amount of cash in the portfolio at inception.
    In current implementation defaults to USD.
    """

    start_datetime: datetime
    """
    The starting timestamp for generating the portfolio time series.
    """

    end_datetime: Optional[datetime] = None
    """
    The ending timestamp for generating the portfolio time series.
    Defaults to latest datetime.
    """

    close_frequency: Optional[
        PortfolioTimeseriesFrequency
    ] = PortfolioTimeseriesFrequency.DAILY
    """
    When generating the position time series, the frequency of balance snapshots.
    Where DAILY, the selected mark_time is used as daily close times.
    """

    mark_time: Optional[MarkTime] = MarkTime.UTC
    """
    The close time convention to use for close-on-close prices in the 24x7 market.
    Defaults to UTC midnight.
    """

    rebalancing_frequency: Optional[RebalancingFrequency] = RebalancingFrequency.DAILY
    """
    Frequency at which the system revaluates positions and weights to bring the
    allocation back in line with the initial_weights.
    """

    @validator("initial_weights")
    def check_initial_weights_sum(cls, values):
        unique_assets = {}
        for ap in values:
            current_asset = unique_assets.get(ap.asset_id)
            current_weight = current_asset.weight if current_asset else 0
            unique_assets[ap.asset_id] = AssetWeight(
                asset_id=ap.asset_id, weight=ap.weight + current_weight
            )
        if round(sum([ap.weight for ap in unique_assets.values()]), 9) != 1:
            raise ValueError("initial_weights do not sum up to 1")
        return list(unique_assets.values())


class PortfolioFromTradesRequest(CamelModel):
    """
    API request to create a portfolio from an initial set of asset position
    and a set of trades and transfers. Trades model buys and sells on exchange
    over the life of the portfolio; transfers model movement of assets in and
    out of the portfolio over its lifetime, including cash moves for subscriptions
    and redemptions where applicable.
    """

    initial_positions: List[AssetPosition]
    """
    Initial quantities of assets contained in the portfolio before trades and
    transfers are applied over time, if any. If you just want to represent an
    unchanging portfolio composition, provide your current positions here with
    no trades or transfers; this lets you conduct a pro forma analysis.
    """

    trades: Optional[Trades] = None
    """
    Optional set of buys and sells to execute from start_datetime to end_datetime.
    """

    transfers: Optional[Transfers] = None
    """
    Optional set of transfers of assets in and out of the portfolio to execute
    from start_datetime to end_datetime.
    """

    start_datetime: datetime
    """
    The starting timestamp for generating the portfolio time series.
    """

    end_datetime: Optional[datetime] = None
    """
    The ending timestamp for generating the portfolio time series.
    Defaults to latest datetime.
    """

    close_frequency: Optional[
        PortfolioTimeseriesFrequency
    ] = PortfolioTimeseriesFrequency.DAILY
    """
    When generating the position time series, the frequency of balance snapshots.
    """

    @validator("initial_positions")
    def merge_duplicated_asset_positions(cls, values):
        unique_assets = {}
        for ap in values:
            current_asset = unique_assets.get(ap.asset_id)
            current_qty = current_asset.quantity if current_asset else 0
            unique_assets[ap.asset_id] = AssetPosition(
                asset_id=ap.asset_id, quantity=ap.quantity + current_qty
            )
        return list(unique_assets.values())


class PortfolioAnalyticRequest(CamelModel):
    """
    API request to compute a set of performance statistics for a given portfolio.
    If simulated_trades are provided, the system will compute twice: once with the
    base portfolio, and again with the base portfolio + simulated_trades applied.
    """

    portfolio: PortfolioCompositionAndTrades
    """
    The base set of positions and trades to use for computing performance statistics.
    """

    simulated_trades: Optional[Trades] = None
    """
    Optional set of trades to overlay on the base portfolio in order to simulate
    the performance impact of a rebalance or other portfolio composition change.
    """

    benchmarks: Optional[Dict[str, Union[PortfolioComposition, CustomizedPortfolioComposition]]] = None
    """
    For benchmark-relative measures, which benchmark indices, baskets or assets
    should be used for purposes of comparison?
    """

    compounding_frequency: Optional[CompoundingFrequencyInput] = CompoundingFrequencyInput.DAILY
    """
    Where using logarithmic returns, how frequently are the returns compounded?
    Where DAILY, the selected mark_time is used as daily close times.
    """

    mark_time: Optional[MarkTime] = MarkTime.UTC
    """
    The close time convention to use for close-on-close prices in the 24x7 market.
    Defaults to UTC midnight.
    """

    returns_type: Optional[ReturnsType] = ReturnsType.SIMPLE
    """
    Calculation treatment for portfolio returns.
    """


class BrinsonAttributionRequest(CamelModel):
    """
    API request to compute brinson attribution of a given portfolio.
    """

    portfolio: PortfolioCompositionAndTrades
    """
    The base set of positions and trades to use for computing brinson attribution.
    """

    benchmarks: Optional[Dict[str, Union[PortfolioComposition, CustomizedPortfolioComposition]]] = None
    """
    The benchmarks used to compute the relative measures against portfolio
    """

    compounding_frequency: Optional[CompoundingFrequencyInput] = CompoundingFrequencyInput.DAILY
    """
    Where using logarithmic returns, how frequently are the returns compounded?
    Where DAILY, the selected mark_time is used as daily close times.
    """

    mark_time: Optional[MarkTime] = MarkTime.UTC
    """
    The close time convention to use for close-on-close prices in the 24x7 market.
    Defaults to UTC midnight.
    """

    returns_type: Optional[ReturnsType] = ReturnsType.SIMPLE
    """
    Calculation treatment for portfolio returns.
    """

    sector_taxonomy_id: Optional[UUID] = None
    """
    Specify which sector taxonomy provider's UUID to be used. Defaults to DACS's UUID.
    """


class PortfolioAnalyticSimpleReturn(CamelModel):
    """
    Value object carrying return measures based on simple returns, the percentage change in the value of
    the portfolio's constituents from its initial value to its final value.
    """

    cumulative_return: NumberOrNanReplacement
    """
    The total amount of growth or change in value of an investment over a specific period, calculated by considering
    all gains and losses during that timeframe. It represents the net effect of multiple returns, showcasing the
    overall performance and change in value of the investment from its starting point to the end of the period.
    """

    annualised_return: NumberOrNanReplacement
    """
    The average rate of growth or change in value of an investment expressed as an annual percentage. It considers
    the compound effect of returns over multiple periods to provide a standardized measure of performance over time,
    facilitating comparison between investments with different holding periods.
    """


class PortfolioAnalyticLogReturn(CamelModel):
    """
    Value object carrying portfolio return measures based on continuously compounded or logarithmic returns.
    """

    cumulative_return: NumberOrNanReplacement
    """
    The total growth or change in value of an investment over a specific period, calculated by summing the
    logarithmic returns for each subperiod within that timeframe. This approach accurately reflects the
    compounding effect of returns over time and provides a more precise representation of overall
    investment performance, especially for extended periods.
    """

    annualised_return: NumberOrNanReplacement
    """
    The average rate of growth or change in value of an investment per year, calculated by compounding
    the logarithmic returns over the entire holding period and then converting the result into an
    annualized percentage. This method accounts for the compounding effect of returns over time and
    provides a standardized measure of performance, suitable for comparing investments with
    varying holding periods.
    """

    returns_by_period: Dict[datetime, NumberOrNanReplacement]
    """
    Breakdown of logarithmic returns by reporting period.
    """


class PortfolioAnalyticAbsolutePerformance(CamelModel):
    """
    Value object carrying various measures of absolute portfolio performance,
    independent of the chosen benchmark(s).
    """

    sharpe_ratio: NumberOrNanReplacement
    """
    A measure that evaluates the risk-adjusted return of an investment by considering the excess return earned per
    unit of volatility, helping to assess the efficiency of returns relative to the level of risk taken.
    """

    sortino_ratio: NumberOrNanReplacement
    """
    A risk-adjusted performance metric that focuses on downside volatility by measuring the excess return per unit of
    downside risk, providing insight into an investment's ability to generate positive returns while minimizing
    downside fluctuations.
    """

    calmar_ratio: NumberOrNanReplacement
    """
    A ratio used to gauge the risk-adjusted performance of an investment by comparing the average annual return
    to the maximum drawdown experienced over a specific time frame, indicating the ability to generate returns
    relative to the depth of losses.
    """

    max_drawdown: NumberOrNanReplacement
    """
    The largest peak-to-trough decline in the value of an investment or portfolio during a specific period,
    revealing the extent of loss from the highest point to the lowest point reached.
    """


class PortfolioAnalyticVolatility(CamelModel):
    """
    Value object for carrying the various portfolio volatility measures.
    """

    annualised_volatility: NumberOrNanReplacement
    """
    Portfolio returns volatility, expressed as a fraction.
    """

    upside_volatility: NumberOrNanReplacement
    """
    Portfolio returns volatility limited to the positive variations from average,
    the right tail of the distribution, expressed as a fraction.
    """

    downside_volatility: NumberOrNanReplacement
    """
    Portfolio returns volatility limited to the negative variations from average,
    the right tail of the distribution, expressed as a fraction.
    """


class PortfolioAnalyticRelativePerformance(CamelModel):
    """
    Benchmark-relative measures of portfolio performance.
    """

    annualised_active_premium: NumberOrNanReplacement
    """
    The yearly average difference in returns between a portfolio and its benchmark index,
    reflecting the active management's impact on performance after accountingfor market movements.
    """

    tracking_error: NumberOrNanReplacement
    """
    The standard deviation of the variance between a portfolio's returns and those of its benchmark index,
    measuring the extent to which the portfolio's performance deviates from the benchmark.
    """

    information_ratio: NumberOrNanReplacement
    """
    A ratio that assesses an investment manager's ability to generate excess returns relative
    to the level of risk taken, by comparing the portfolio's active return with its tracking error.
    """

    relative_beta: NumberOrNanReplacement
    """
    The measure of an asset's sensitivity to market movements compared to a chosen benchmark index,
    indicating how much the asset's price tends to move relative to the benchmark's movements.
    """

    upside_capture_ratio: NumberOrNanReplacement
    """
    The ratio of a portfolio's positive returns compared to its benchmark's positive returns,
    showcasing the portfolio's ability to capture gains during favorable market conditions.
    """

    downside_capture_ratio: NumberOrNanReplacement
    """
    The ratio of a portfolio's negative returns compared to its benchmark's negative returns,
    demonstrating the portfolio's susceptibility to losses during unfavorable market conditions.
    """

    excess_max_drawdown: NumberOrNanReplacement
    """
    The difference between a portfolio's maximum drawdown (peak-to-trough decline) and the
    corresponding drawdown of its benchmark index, highlighting how much worse the portfolio's
    losses were compared to the benchmark during its worst period.
    """


class BrinsonAttributionExposure(CamelModel):
    """
    Portfolio and benchmarks exposure (compounded over time), by sector.
    """

    sectors: List[str]
    """
    List of sectors.
    """

    portfolio: List[NumberOrNanReplacement]
    """
    Portfolio's exposure (compounded over time), by sector.
    """

    benchmark: List[NumberOrNanReplacement]
    """
    Benchmark's exposure (compounded over time), by sector.
    """

    difference: List[NumberOrNanReplacement]
    """
    Difference between portfolio and benchmark exposure.
    """


class BrinsonAttribution(CamelModel):
    """
    Brinson attribution results.
    """

    exposures: BrinsonAttributionExposure
    """
    Calculated portfolio and benchmarks exposure (compounded over time), by sector.
    """

    as_of_time: List[datetime]
    """
    Series of timestamps corresponding to the start of each reporting period.
    """

    allocation: List[NumberOrNanReplacement]
    """
    Calculatd portfolio's allocation return. Allocation refers to the value the portfolio
    manager adds by having different sector weights in the portfolio than the sector weights in
    the benchmark.
    """

    selection: List[NumberOrNanReplacement]
    """
    Calculated portfolio's selection return. Selection refers to the value the portfolio
    manager adds by holding individual securities or instruments within the sector in
    different-than-benchmark weights.
    """

    interaction: List[NumberOrNanReplacement]
    """
    Calculates portfolio's interaction return. Interaction is a directly calculable effect
    resulting from the combination of (or interaction between) allocation and selection effects.
    """

    active_return: List[NumberOrNanReplacement]
    """
    Calculated portfolio's active return. Active return is a directly calculable effect
    resulting from the sum of all, allocation, selection and interaction effects. It is also
    a direct measure of portfolio performance, relative to a benchmark.
    """


class PortfolioAnalyticSummary(CamelModel):
    """
    Value object carrying the highest-level summaries of portfolio performance.
    """

    as_of_time: List[datetime]
    """
    Series of timestamps corresponding to the start of each reporting period.
    """

    trading_pnl: List[NumberOrNanReplacement]
    """
    P&L due to trades within the period.
    """

    holding_pnl: List[NumberOrNanReplacement]
    """
    P&L resulted from holdin position from previous period end.
    """

    commission: List[NumberOrNanReplacement]
    """
    Total commission for the period.
    """

    net_pnl: List[NumberOrNanReplacement]
    """
    Series of net P&L measures for the portfolio, accounting for both trading
    P&L and the increase or decrease in the value of the assets held.
    """

    buy_amount: List[NumberOrNanReplacement]
    """
    Total asset value bought in the period.
    """

    sell_amount: List[NumberOrNanReplacement]
    """
    Total asset value sold in the period.
    """

    trade_amount: List[NumberOrNanReplacement]
    """
    Sum of buy amount and sell amount in the period.
    """

    transfer_amount: List[NumberOrNanReplacement]
    """
    Total amount transfered in or out of the portfolio in the period.
    """

    total_pnl: List[NumberOrNanReplacement]
    """
    Cumulative net P&L till given period.
    """

    long_amount: List[NumberOrNanReplacement]
    """
    Total long position values.
    """

    short_amount: List[NumberOrNanReplacement]
    """
    Total short position values.
    """

    cash_change: List[NumberOrNanReplacement]
    """
    Cash position change in the period.
    """

    cash: List[NumberOrNanReplacement]
    """
    Total cash position as of period end.
    """

    gmv: List[NumberOrNanReplacement]
    """
    Series of gross market values of the assets held over time.
    """

    npv: List[NumberOrNanReplacement]
    """
    Series of net market values of the assets held over time.
    """


class PortfolioAnalyticStatistics(CamelModel):
    """
    Simple distributional measures of the portfolio returns.
    """

    mean: NumberOrNanReplacement
    """
    Average value in the distribution of portfolio returns.
    """

    stddev: NumberOrNanReplacement
    """
    Standard deviation in the distribution of portfolio returns.
    """

    skew: NumberOrNanReplacement
    """
    Skewness measures the asymmetry of the probability distribution of portfolio returns.
    Positive skew indicates that the distribution has a longer tail on the right,
    implying more extreme positive returns, while negative skew implies a longer tail on the left,
    suggesting more extreme negative returns. Skewness helps assess the potential for returns
    to deviate from the average in one direction.
    """

    kurtosis: NumberOrNanReplacement
    """
    Kurtosis gauges the thickness of the tails and the concentration of returns around the mean in the
    probability distribution of portfolio returns. High kurtosis indicates heavy tails and a greater
    concentration of returns, potentially leading to more frequent extreme values. Low kurtosis implies
    lighter tails and less concentration around the mean. Kurtosis offers insights into the likelihood
    of extreme events and the overall shape of the return distribution.
    """


class PortfolioAnalyticStatisticsGroup(CamelModel):
    """
    Value object that groups the performance statistics by portfolio and constituent asset.
    """

    by_portfolios: Dict[str, PortfolioAnalyticStatistics]
    """
    Grouping of portfolio statistics by portfolio ID.
    """

    by_assets: Dict[Union[UUID, str], PortfolioAnalyticStatistics]
    """
    Grouping of portfolio statistics by unique asset ID.
    """


class PortfolioAnalyticPearsonCorrelationGroup(CamelModel):
    """
    Value object that groups correlation results by portfolio and constituent asset.
    """

    by_portfolios: Optional[Dict[str, Dict[str, NumberOrNanReplacement]]]
    """
    Grouping of pairwise portfolio correlations by portfolio ID.
    """

    by_assets: Dict[Union[UUID, str], Dict[Union[UUID, str], NumberOrNanReplacement]]
    """
    Grouping of pairwise asset correlations by asset ID.
    """


class PortfolioAnalyticResult(CamelModel):
    """
    Value object combining various portfolio performance statistics
    by type for a single portfolio.
    """

    summary: PortfolioAnalyticSummary
    """
    High-level P&L summary for this portfolio.
    """

    returns: Dict[str, PortfolioAnalyticSimpleReturn]
    """
    For each portfolio analyzed provide a summary of the returns using simple
    returns only for now. Log returns will be supported in a subsequent release.
    """

    volatility: Dict[str, PortfolioAnalyticVolatility]
    """
    For each portfolio analyzed provide a summary of the volatility measures.
    """

    statistics: PortfolioAnalyticStatisticsGroup
    """
    For each portfolio analyzed provide a summary of basic ratios, drawdown, etc..
    """

    pearson_correlation: PortfolioAnalyticPearsonCorrelationGroup
    """
    Pairwise correlations by portfolio and asset.
    """

    absolute_performance: PortfolioAnalyticAbsolutePerformance
    """
    Absolute perforamnce measures for the input portfolio.
    """

    relative_performance: Optional[Dict[str, PortfolioAnalyticRelativePerformance]]
    """
    For each benchmark provided, a summary of the benchmark-relative performance.
    """


class PortfolioAnalyticOutput(CamelModel):
    """
    Value object carrying a combination of the base results and
    the results from running the analytics with the portfolio
    plus the simulated_trades.
    """
    base_results: PortfolioAnalyticResult
    """
    Results without the simulated trades.
    """

    simulated_results: Optional[PortfolioAnalyticResult]
    """
    Results with the simulated trades, if provided.
    """


class BrinsonAttributionOutput(CamelModel):
    """
    Value object carrying the result of brinson attribution against each benchmarks.
    """
    by_benchmark: Dict[str, BrinsonAttribution]
