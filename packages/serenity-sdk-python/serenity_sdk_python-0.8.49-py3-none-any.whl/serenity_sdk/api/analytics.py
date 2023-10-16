import json

from serenity_sdk.api.core import CallType, SerenityApi, SerenityClient
from serenity_types.utils.common import Response
from serenity_types.valuation.core import PortfolioTimeseriesAndTrades
from serenity_types.valuation.portfolio_analytic import (
    BrinsonAttributionOutput,
    BrinsonAttributionRequest,
    PortfolioAnalyticOutput,
    PortfolioAnalyticRequest,
    PortfolioFromAllocationRequest,
    PortfolioFromTradesRequest,
)


class PortfolioAnalyticsApi(SerenityApi):
    """
    Helper class for the Portfolio Analytics API, which lets clients create portfolios
    parametrically and then run performance analysis on those rich portfolios, both
    basic portfolio statistics (Sharpe, Sortino, max drawdown, etc.) and more sophisticated
    Brinson single- and multi-period portfolio performance attribution.
    """

    def __init__(self, client: SerenityClient):
        """
        :param client: the raw client to delegate to when making API calls
        """

        # NOTE: I don't think the base endpoint should be valuation in the future but
        # understand this is the most practical arrangement to start; however, the
        # SDK client at least should be independent from valuation.
        super().__init__(client, "valuation")

    def create_portfolio_from_allocation(
        self, request: PortfolioFromAllocationRequest
    ) -> Response[PortfolioTimeseriesAndTrades]:
        """
        Given a set of weights and a rebalancing frequency, takes an initial
        cash position, trades into it, and periodically rebalances. The output
        is the portfolio positions and trades.
        """
        req_json = json.loads(request.json(exclude_unset=True, by_alias=True))
        raw_json = self._call_api(
            api_path="/portfolio/create/from_allocation",
            body_json=req_json,
            call_type=CallType.POST,
        )
        result = PortfolioTimeseriesAndTrades.parse_obj(raw_json["result"])
        return SerenityApi._create_response_object(raw_json, result)

    def create_portfolio_from_trades(
        self, request: PortfolioFromTradesRequest
    ) -> Response[PortfolioTimeseriesAndTrades]:
        """
        Given an initial set of positions and a series of trades and transfers
        plus the frequency of closing snapshots (e.g. daily close), produces a full
        portfolio object with the timeseries of positions and trades.
        """
        req_json = json.loads(request.json(exclude_unset=True, by_alias=True))
        raw_json = self._call_api(
            api_path="/portfolio/create/from_trades",
            body_json=req_json,
            call_type=CallType.POST,
        )
        result = PortfolioTimeseriesAndTrades.parse_obj(raw_json["result"])
        return SerenityApi._create_response_object(raw_json, result)

    def compute_portfolio_statistics(
        self, request: PortfolioAnalyticRequest
    ) -> Response[PortfolioAnalyticOutput]:
        """
        Given a rich portfolio object with periodic positions, trades and transfers,
        computes standard portfolio analytics like Sharpe, Sortino, max drawdown, etc..
        Optionally you can also include a set of "simulated trades" so you can see
        how portfolio performance would differ if you execute those trades, essentially
        perform a what-if analysis on past trading decisions or alternative portfolios.
        """
        req_json = json.loads(request.json(exclude_unset=True, by_alias=True))
        raw_json = self._call_api(
            api_path="/portfolio/analytic/compute",
            body_json=req_json,
            call_type=CallType.POST,
        )
        result = PortfolioAnalyticOutput.parse_obj(raw_json["result"])
        return SerenityApi._create_response_object(raw_json, result)

    def compute_portfolio_performance_attribution(
        self, request: BrinsonAttributionRequest
    ) -> Response[BrinsonAttributionOutput]:
        """
        Given a rich portfolio object with periodic positions, trades and transfers,
        computes the Brinson performance attribution, assessing to what degree the
        performance is due to active management.
        """
        req_json = json.loads(request.json(exclude_unset=True, by_alias=True))
        raw_json = self._call_api(
            api_path="/portfolio/brinson_attribution",
            body_json=req_json,
            call_type=CallType.POST,
        )
        result = BrinsonAttributionOutput.parse_obj(raw_json["result"])
        return SerenityApi._create_response_object(raw_json, result)
