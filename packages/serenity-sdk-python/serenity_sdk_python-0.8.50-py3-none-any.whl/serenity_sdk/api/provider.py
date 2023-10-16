from serenity_sdk.api.model import ModelApi
from serenity_sdk.api.account import AccountApi
from serenity_sdk.api.analytics import PortfolioAnalyticsApi
from serenity_sdk.api.portfolio import PortfolioApi
from serenity_sdk.api.pricing import PricerApi
from serenity_sdk.api.refdata import RefdataApi
from serenity_sdk.api.risk import RiskApi
from serenity_sdk.api.scenarios import ScenariosApi
from serenity_sdk.api.valuation import ValuationApi
from serenity_sdk.client.raw import SerenityClient


class SerenityApiProvider:
    """
    Simple entrypoint that gives you access to the full set of Serenity API's from a single class.
    """
    def __init__(self, client: SerenityClient):
        """
        :param client: the raw client to wrap around for every typed endpoint
        """

        self.refdata_api = RefdataApi(client)
        self.risk_api = RiskApi(client)
        self.valuation_api = ValuationApi(client)
        self.pricer_api = PricerApi(client)
        self.model_api = ModelApi(client)
        self.scenarios_api = ScenariosApi(client)
        self.account_api = AccountApi(client)
        self.portfolio_api = PortfolioApi(client)
        self.portfolio_analytics_api = PortfolioAnalyticsApi(client)

    def refdata(self) -> RefdataApi:
        """
        Gets a typed wrapper around all the supported reference data API calls.
        """
        return self.refdata_api

    def risk(self) -> RiskApi:
        """
        Gets a typed wrapper aorund all the supported risk-related API calls. Currently this mixes
        factor risk attribution and VaR-related calls, but we may break this out later.
        """
        return self.risk_api

    def valuation(self) -> ValuationApi:
        """
        Gets a typed wrapper for all the portfolio valuation API functions.
        """
        return self.valuation_api

    def pricer(self) -> PricerApi:
        """
        Gets a typed wrapper for all the pricing API's for derivatives.
        """
        return self.pricer_api

    def scenarios(self) -> ScenariosApi:
        """
        Gets a typed wrapper for executing scenarios and managing custom scenarios.
        """
        return self.scenarios_api

    def model(self) -> ModelApi:
        """
        Gets a typed wrapper for all the ModelOps (model metadata) API functions.
        """
        return self.model_api

    def portfolio(self) -> PortfolioApi:
        """
        Gets a typed wrapper for all the Portfolio Storage API functions.
        """
        return self.portfolio_api

    def account(self) -> AccountApi:
        """
        Gets a typed wrapper for all the Account API functions.
        """
        return self.account_api

    def portfolio_analytics(self) -> PortfolioAnalyticsApi:
        """
        Gets a typed wrapper for all the Portfolio Analytics functions.
        """
        return self.portfolio_analytics_api
