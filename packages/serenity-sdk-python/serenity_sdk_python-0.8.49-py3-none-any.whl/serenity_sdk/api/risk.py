import json
from typing import Any, Dict, Optional
from uuid import UUID

import pandas as pd
from pandas.io.formats.style import Styler

from serenity_sdk.api.core import SerenityApi
from serenity_sdk.client.raw import CallType, SerenityClient
from serenity_sdk.types.common import STD_DATE_FMT, STD_DATETIME_FMT, CalculationContext, Portfolio
from serenity_sdk.types.refdata import AssetMaster
from serenity_sdk.types.factors import RiskAttributionResult
from serenity_sdk.types.measures import RiskMeasureContext
from serenity_types.risk.measures import PortfolioRiskResponse


class RiskApi(SerenityApi):
    """
    The risk API group covers risk attribution, VaR and (in a future release) scenario analysis.
    """

    def __init__(self, client: SerenityClient):
        """
        :param client: the raw client to delegate to when making API calls
        """
        super().__init__(client, 'risk')

    def compute_risk_attrib(self, ctx: CalculationContext,
                            portfolio: Portfolio,
                            sector_taxonomy_id: Optional[UUID] = None) -> RiskAttributionResult:
        """
        Given a portfolio, breaks down the volatility and variance of the portfolio in various
        slices, e.g. by asset, by sector & asset, by sector & factor, and by factor. These different
        pivots of the risk can help you identify areas of risk concentration. All risk calculations
        are always as of a given date, which among other things determines precomputed model values
        that will be applied, e.g. for a factor risk model, as-of date determines the factor loadings.

        Note that sector_taxonomy support will be dropped with the next release, once the refdata endpoint
        for looking up sector_taxonomy_id is available.

        :param ctx: the common risk calculation parameters to use, e.g. as-of date or factor risk model ID
        :param portfolio: the portfolio on which to perform risk attribution
        :param sector_taxonomy_id: the unique ID of the sector taxonomy for pivoting, else DACS if None
        :return: a typed wrapper around the risk attribution results
        """
        body_json = {
            **self._create_std_params(ctx.as_of_date),
            'portfolio': {'assetPositions': portfolio.to_asset_positions()},
            'modelConfigId': str(ctx.model_config_id),
            'assetPositions': portfolio.to_asset_positions()
        }
        risk_attribution_json = self._call_api('/market/factor/attribution', {}, body_json, CallType.POST)
        result = RiskAttributionResult(risk_attribution_json)
        return result

    def compute_risk_measures(
        self, ctx: RiskMeasureContext, portfolio: Portfolio
    ) -> PortfolioRiskResponse:
        """
        Computes risk measures for a portfolio.
        :param ctx: request and as_of_time
        :param portfolio: the portfolio to calculate risk measures for
        """
        request = {
            "portfolio": portfolio.to_asset_positions(),
            "asOfTime": ctx.as_of_time.strftime(STD_DATETIME_FMT),
            "riskComputationRequest": json.loads(
                ctx.request.json(exclude_unset=True, by_alias=True)
            ),
        }

        #        request_json = json.loads(request.json(exclude_unset=True, by_alias=True))
        raw_json = self._call_api("/measures/compute", {}, request, CallType.POST)

        return PortfolioRiskResponse.parse_obj(raw_json["result"])

    def get_asset_covariance_matrix(self, ctx: CalculationContext, asset_master: AssetMaster,
                                    portfolio: Optional[Portfolio] = None) -> pd.DataFrame:
        """
        Gets the asset covariance matrix with asset ID's translated to native symbols, as a DataFrame.

        :param ctx: the common risk calculation parameters to use, specifically the as-of date and model ID in this case
        :return: a DataFrame pivoted by `assetId1` and `assetId2` with the asset covariance `value` as a column
        """
        params = RiskApi._create_get_params(ctx)
        raw_json = self._call_api('/market/factor/asset_covariance', params)
        return RiskApi._asset_matrix_to_dataframe(raw_json['matrix'], asset_master, portfolio)

    def get_asset_residual_covariance_matrix(self, ctx: CalculationContext, asset_master: AssetMaster,
                                             portfolio: Optional[Portfolio] = None) -> pd.DataFrame:
        """
        Gets the asset residual covariance matrix with asset ID's translated to native symbols, as a DataFrame.

        :param ctx: the common risk calculation parameters to use, specifically the as-of date and model ID in this case
        :return: a DataFrame pivoted by `assetId1` and `assetId2` with the asset residual `value` as a column
        """
        params = RiskApi._create_get_params(ctx)
        ids_dict = portfolio.get_assets() if portfolio else {}
        raw_json = self._call_api('/market/factor/residual_covariance', params)
        rows = [{'assetId': element['assetId1'],
                 'symbol': asset_master.get_symbol_by_id(UUID(element['assetId1'])),
                 'value': element['value']} for element in raw_json['matrix']
                if (len(ids_dict) == 0) or UUID(element['assetId1']) in ids_dict.keys()]
        return pd.DataFrame(rows)

    def get_factor_correlation_matrix(self, ctx: CalculationContext) -> pd.DataFrame:
        """
        Gets the factor correlation matrix.

        :param ctx: the common risk calculation parameters to use, specifically the as-of date and model ID in this case
        :return: a DataFrame pivoted by `factor1` and `factor2` with the
            factor correlation coefficient `value` as a column
        """
        params = RiskApi._create_get_params(ctx)
        raw_json = self._call_api('/market/factor/correlation', params)
        return RiskApi._factor_matrix_to_dataframe(raw_json['matrix'])

    def get_factor_covariance_matrix(self, ctx: CalculationContext) -> pd.DataFrame:
        """
        Gets the factor covariance matrix.

        :param ctx: the common risk calculation parameters to use, specifically the as-of date and model ID in this case
        :return: a DataFrame pivoted by `factor1` and `factor2` with the factor covariance `value` as a column
        """
        params = RiskApi._create_get_params(ctx)
        raw_json = self._call_api('/market/factor/covariance', params)
        return RiskApi._factor_matrix_to_dataframe(raw_json['matrix'])

    def get_asset_factor_exposures(self, ctx: CalculationContext, asset_master: AssetMaster,
                                   portfolio: Optional[Portfolio] = None) -> pd.DataFrame:
        """
        Gets the factor exposures by assets as a DataFrame.

        :param ctx: the common risk calculation parameters to use, specifically the as-of date and model ID in this case
        :param asset_master: an AssetMaster to use to resolve UUID to native symbols
        :param portfolio: optional Portfolio used to subset the matrix to just assets in the portfolio
        :return: a DataFrame pivoted by `assetId` and `factor` with the exposure `value` as a column
        """
        def map_asset_id(asset_id: str):
            return asset_master.get_symbol_by_id(UUID(asset_id))

        params = RiskApi._create_get_params(ctx)
        raw_json = self._call_api('/market/factor/exposures', params)
        factor_exposures = pd.DataFrame.from_dict(raw_json['matrix'])
        if portfolio:
            ids_dict = portfolio.get_assets()
            pf_ids = [str(asset_id) for asset_id in ids_dict.keys()]
            factor_exposures = factor_exposures[factor_exposures['assetId'].isin(pf_ids)]

        factor_exposures = factor_exposures.pivot(index='assetId', columns='factor', values='value')
        factor_exposures.set_index(factor_exposures.index.map(map_asset_id), inplace=True)

        return factor_exposures

    def get_factor_returns(self, ctx: CalculationContext) -> Styler:
        """
        Gets the factor returns as a DataFrame.

        :param ctx: the common risk calculation parameters to use, specifically the as-of date and model ID in this case
        :return: a DataFrame indexed by `closeDate` and `factor` with the return `value` as a column
        """
        params = RiskApi._create_get_params(ctx)
        raw_json = self._call_api('/market/factor/returns', params)
        factor_returns = pd.DataFrame.from_dict(raw_json['factorReturns']).pivot(index='closeDate', columns='factor',
                                                                                 values='value')
        return factor_returns.style.format("{:.1%}")

    def get_factor_portfolios(self, ctx: CalculationContext) -> Dict[str, Portfolio]:
        """
        Gets the factor index compositions for each factor.

        :param ctx: the common risk calculation parameters to use, specifically the as-of date and model ID in this case
        :return: a mapping from factor name to the factor portfolio
        """
        params = RiskApi._create_get_params(ctx)
        raw_json = self._call_api('/market/factor/indexcomps', params)
        factors = {factor: RiskApi._to_portfolio(indexcomps) for (factor, indexcomps) in raw_json['factors'].items()}
        return factors

    @staticmethod
    def _asset_matrix_to_dataframe(matrix_json: Any, asset_master: AssetMaster,
                                   portfolio: Optional[Portfolio] = None) -> pd.DataFrame:
        """
        Converts an asset matrix (asset pairs and values) into a simple DataFrame

        :param matrix_json: the raw matrix output from the API
        :param asset_master: a loaded AssetMaster to convert UUID to symbols
        :param portfolio: an optional portfolio to use to subset the matrix
        :return: a DataFrame pivoted by `assetId1` and `assetId2` with `value` columns
        """
        def map_asset_id(asset_id: str):
            return asset_master.get_symbol_by_id(UUID(asset_id))

        df = pd.DataFrame.from_dict(matrix_json).dropna()
        if portfolio:
            ids_dict = portfolio.get_assets()
            pf_ids = [str(asset_id) for asset_id in ids_dict.keys()]
            df = df[df['assetId1'].isin(pf_ids) &
                    df['assetId2'].isin(pf_ids)]
        df = df.pivot(index='assetId1', columns='assetId2', values='value')
        df.set_index(df.index.map(map_asset_id), inplace=True)
        df.columns = df.columns.map(map_asset_id)

        return df

    @staticmethod
    def _factor_matrix_to_dataframe(matrix_json: Any) -> pd.DataFrame:
        """
        Converts a factor matrix (factor pairs and values) into a simple DataFrame

        :param matrix_json: _description_
        :return: a DataFrame pivoted by `factor1` and `factor2` with `value` columns
        """
        df = pd.DataFrame.from_dict(matrix_json).dropna()
        df = df.pivot(index='factor1', columns='factor2', values='value')
        return df

    @staticmethod
    def _to_portfolio(indexcomps: Any) -> Portfolio:
        """
        Converts raw factor index composition data in JSON format to a typed Portfolio object.

        :param indexcomps: _description_
        :return: the typed Portfolio object
        """
        positions = {UUID(entry['assetId']): entry['weight'] for entry in indexcomps if entry['weight'] != 0}
        return Portfolio(positions)

    @staticmethod
    def _create_get_params(ctx: CalculationContext) -> Dict[str, Any]:
        """
        Creates the full set of GET-style parameters given a :class:`CalculationContext`.

        :param ctx: the bundle of calculation defaults, e.g. base currency to use
        :return: the full set of call parameters
        """
        return {
            'as_of_date': ctx.as_of_date.strftime(STD_DATE_FMT),
            'model_config_id': ctx.model_config_id
        }
