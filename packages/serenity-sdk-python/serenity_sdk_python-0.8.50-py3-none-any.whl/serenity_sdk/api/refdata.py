import json
from datetime import date
from typing import Any, AnyStr, Dict, List, Optional
from uuid import UUID

from serenity_sdk.api.core import SerenityApi
from serenity_sdk.client.raw import CallType, SerenityClient
from serenity_sdk.types.refdata import AssetMaster
from serenity_types.refdata.asset import Asset, AssetSearchRequest, AssetType
from serenity_types.refdata.currency import Currency
from serenity_types.refdata.futures import Future, Perpetual
from serenity_types.refdata.options import ListedOption
from serenity_types.refdata.token import TokenAsset

ASSET_MAPPING = {
    AssetType.CURRENCY.value: Currency,
    AssetType.FUTURE.value: Future,
    AssetType.LISTED_OPTION.value: ListedOption,
    AssetType.PERPETUAL.value: Perpetual,
    AssetType.TOKEN.value: TokenAsset
}


class RefdataApi(SerenityApi):
    """
    The refdata API group covers access to the Serenity Asset Master and other supporting
    reference data needed for constructing portfolios and running risk models.
    """

    def __init__(self, client: SerenityClient):
        """
        :param client: the raw client to delegate to when making API calls
        """
        super().__init__(client, 'refdata')

    def load_asset_master(self, as_of_date: Optional[date] = None) -> AssetMaster:
        """
        Bulk load operation that loads the whole asset master into memory so it can be
        used to help build portfolios bassed on inputs in different symbologies, and
        so it can be queried without hitting the server multiple times. Reference data
        is always as of a date, as it can change over time, but if a date is not provided
        the system will default to the latest date.

        :param as_of_date: the effective date for all loaded refdata, else latest if None
        :return: an :class:`AssetMaster` object containing all asset-linked reference data
        """
        asset_summaries = self.get_asset_summaries(as_of_date)
        return AssetMaster(asset_summaries)

    def get_asset_summaries(self, as_of_date: Optional[date] = None) -> List[Any]:
        """
        Gets the list of asset records in the asset master. In general you should prefer
        to use :func:`load_asset_master` instead, which will help parsing the JSON records,
        rather than this lower-level call.

        :param as_of_date: the effective date for all loaded refdata, else latest if None
        :return: a list of JSON-formatted asset summary objects
        """
        params = self._create_std_params(as_of_date)
        resp = self._call_api('/asset/summaries', params)
        asset_summaries = resp['assetSummary']
        return asset_summaries

    def get_asset_types(self, as_of_date: Optional[date] = None) -> Dict[AnyStr, AnyStr]:
        """
        Gets the list of supported asset types in the system, e.g. TOKEN

        :return: a map from name to description
        """
        params = self._create_std_params(as_of_date)
        resp = self._call_api('/asset/types', params)
        asset_types = resp['assetType']
        return {asset_type['name']: asset_type['description'] for asset_type in asset_types}

    def get_exchanges(self, as_of_date: Optional[date] = None) -> Dict[str, UUID]:
        """
        Gets the list of supported exchanges in the system, e.g. BINANCE

        :return: a list of exchange objects
        """
        params = self._create_std_params(as_of_date)
        resp = self._call_api('/organization/exchanges', params)
        return {exchange['shortName']: exchange['organizationId']
                for exchange in resp['organization']
                }

    def get_symbol_authorities(self, as_of_date: Optional[date] = None) -> Dict[AnyStr, AnyStr]:
        """
        Gets the list of supported symbol authorities, e.g. KAIKO, DAR or COINGECKO

        :return: a map from name to description
        """
        params = self._create_std_params(as_of_date)
        resp = self._call_api('/symbol/authorities', params)
        authorities = resp['symbolAuthority']
        return {authority['name']: authority['description'] for authority in authorities}

    def get_sector_taxonomies(self, as_of_date: Optional[date] = None) -> Dict[str, UUID]:
        """
        Gets a mapping from a short key like DACS or DATS to the sectory taxonomy ID (UUID).
        This will be required in the next release if you wish to override the sector
        taxonomy in use for risk attribution.

        :return: a map from taxonomy short name to taxonomy UUID
        """
        params = self._create_std_params(as_of_date)
        resp = self._call_api('/sector/taxonomies', params)
        taxonomies = resp['sectorTaxonomy']
        return {taxonomy['name']: taxonomy['taxonomyId'] for taxonomy in taxonomies}

    def search_assets(self, request: AssetSearchRequest) -> List[Asset]:
        """
        Searches the asset master and returns the typed description of the assets
        for *any* :class:serenity_types.refdata.asset.AssetType matching the search criteria.

        :param request: search parameters used to query the backend
        :return: a list of type-specific descriptions matching the query
        """
        req_json = json.loads(request.json())
        resp = self._call_api('/asset/search', {}, req_json, CallType.POST)
        assets = [ASSET_MAPPING[data['assetType']](**data) for data in resp["result"]]
        return assets

    def get_currency(self, iso_currency_code: str) -> Currency:
        """
        A convenience method that wraps the :func:`search_assets` call underneath to
        return the :class:`serenity_types.refdata.currency.Currency` based on the the `iso_currency_code`.

        :param iso_currency_code: the ISO currency code to get. The param is **case_sensitive**.
            E.g **USD** https://www.iban.com/currency-codes
        :return: the :class:`serenity_types.refdata.currency.Currency` that matches the ISO code
        """
        if iso_currency_code:
            request = AssetSearchRequest(asset_types=[AssetType.CURRENCY])
            currencies = self.search_assets(request)
            for cur in (Currency.parse_obj(c) for c in currencies):
                if cur.iso_currency_code == iso_currency_code:
                    return cur
        raise ValueError(f"The currency '{iso_currency_code}' is not supported. "
                         "Please note that the ISO code is case sensitive.")

    def get_tokens(self, native_symbols: List[str]) -> Dict[str, TokenAsset]:
        """
        A convenience method that wraps the :func:`search_assets` call underneath to
        return the :class:`serenity_types.refdata.token.TokenAsset` based on the the `native_symbols`.

        :param native_symbols: the list for the tokens to search. Please note that the symbols are **case sensitive**
        :return: a dict with the native_symbol as key and value :class:`serenity_types.refdata.token.TokenAsset`
        """
        if native_symbols:
            request = AssetSearchRequest(asset_types=[AssetType.TOKEN])
            tokens = self.search_assets(request)
            token_mapping = {tok.native_symbol: tok for tok in (TokenAsset.parse_obj(t) for t in tokens)
                             if tok.native_symbol in native_symbols}
            missing_symbols = set(native_symbols) - set(token_mapping.keys())

            if len(missing_symbols) > 0:
                raise ValueError(f"Unable to find tokens the following tokens {missing_symbols}. "
                                 "Please note that symbol is case sensitive.")

            return token_mapping
        raise ValueError(f"{native_symbols} is not a valid input")

    def describe_assets(self, asset_ids: List[UUID]) -> List[Asset]:
        """
        get the description of the assets for *any* :class:serenity_types.refdata.asset.AssetType matching
        the search criteria.

        :param asset_ids: asset ids (uuid in string format)
        :return: dictionary of asset id to asset description
        """
        req_json = json.loads(json.dumps({"assetIds": [str(id) for id in asset_ids]}))
        resp = self._call_api('/asset', {}, req_json, CallType.POST)

        def _parse_asset(data: Dict[str, Any]) -> Asset:
            data_copy: Dict[str, Any] = {}
            for k, v in data.items():
                if v == 'NaT':
                    data_copy[k] = None
                else:
                    data_copy[k] = v
            return ASSET_MAPPING[data_copy["assetType"].upper()](**data_copy)

        return [_parse_asset(data) for data in resp["result"]]
