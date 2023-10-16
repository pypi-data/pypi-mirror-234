from serenity_sdk.api.core import SerenityApi
from serenity_sdk.client.raw import CallType, SerenityClient
from serenity_sdk.types.common import Portfolio
from serenity_sdk.types.valuation import ValuationResult
from serenity_types.portfolio.core import NetDeltaPortfolioPositions
from serenity_types.pricing.core import PricingContext


class ValuationApi(SerenityApi):
    """
    The valuation API group covers basic tools for NAV and other portfolio valuation calcs.
    """
    def __init__(self, client: SerenityClient):
        """
        :param client: the raw client to delegate to when making API calls
        """
        super().__init__(client, 'valuation')

    def compute_portfolio_value(self, ctx: PricingContext, portfolio: Portfolio) -> ValuationResult:
        """
        Computes portfolio NAV and other high-level valuation details at both the portfolio level
        and position-by-position.

        :param ctx: the pricing parameters to use, e.g. which base currency and the as-of date for prices
        :param portfolio: the portfolio to value
        :return: a parsed :class:`ValuationResult` containing all portfolio & position values
        """
        request = {
            'portfolio': {'assetPositions': portfolio.to_asset_positions()},
            'pricing_context': {
                **self._create_std_params(ctx.as_of_date),
                'portfolio': {'assetPositions': portfolio.to_asset_positions()},
                'markTime': ctx.mark_time.value if ctx.mark_time else None,
                'baseCurrencyId': str(ctx.base_currency_id),
                'cashTreatment': ctx.cash_treatment.value if ctx.cash_treatment else None
            }
        }
        raw_json = self._call_api('/portfolio/compute', {}, request, CallType.POST)
        return ValuationResult._parse(raw_json)

    def compute_portfolio_net_delta_value(
            self, ctx: PricingContext, portfolio: Portfolio) -> NetDeltaPortfolioPositions:
        """
        Given a pricing context (mark time, date, base currency) convert the
        net delta equivalent of the given portfolio.

        :param ctx: the pricing parameters to use, e.g. which base currency and the as-of date for prices
        :param portfolio: the portfolio to value
        :return: a parsed :class:`NetDeltaPortfolioPositions` the converted net delta of the asset positions
        """
        request = {
            'portfolio': portfolio.to_asset_positions(),
            'pricing_context': {
                **self._create_std_params(ctx.as_of_time),
                'markTime': ctx.mark_time.value if ctx.mark_time else None,
                'baseCurrencyId': str(ctx.base_currency_id),
                'cashTreatment': ctx.cash_treatment.value if ctx.cash_treatment else None
            }
        }
        raw_json = self._call_api('/portfolio/net_delta', {}, request, CallType.POST)
        return NetDeltaPortfolioPositions(**raw_json['result'])
