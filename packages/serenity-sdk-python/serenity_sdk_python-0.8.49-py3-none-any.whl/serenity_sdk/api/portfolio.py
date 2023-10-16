import json
from typing import List, Optional
from uuid import UUID

from pydantic import parse_obj_as
from serenity_sdk.api.core import SerenityApi
from serenity_sdk.client.raw import CallType, SerenityClient
from serenity_sdk.types.common import Portfolio
from serenity_sdk.types.core import PortfolioAccountBalanceRequest
from serenity_types.portfolio.core import (
    PortfolioMetadata,
    PortfolioMetadataCreateRequest,
    PortfolioMetadataUpdateRequest,
    PortfolioSnapshot,
    PortfolioSnapshotCreateRequest,
    PortfolioSnapshotUpdateRequest,
)
from serenity_types.ledger.balance import Balance


class PortfolioApi(SerenityApi):
    def __init__(self, client: SerenityClient):
        """
        :param client: the raw client to delegate to when making API calls
        """
        super().__init__(client, "org/portfolios")

    def create_portfolio_metadata(
        self, request: PortfolioMetadataCreateRequest
    ) -> PortfolioMetadata:
        """
        Creates a new Portfolio Metadata.

        :param request: the request with the necessary details to create a new `PortfolioMetadata`
        :return: the created `PortfolioMetadata`
        """
        req_json = json.loads(request.json())
        raw_json = self._call_api("/metadata", {}, req_json, CallType.POST)
        return PortfolioMetadata.parse_obj(raw_json["result"])

    def list_portfolio_metadata(
        self, offset: Optional[int] = 0, limit: Optional[int] = 1000
    ) -> List[PortfolioMetadata]:
        """
        List all `PortfolioMetadata` not marked as deleted.

        :param offset: the number of records to skip in the page.
        :param limit: the maximum number of items that should be returned.
        :return: a list `PortfolioMetadata`
        """
        params = {"offset": str(offset), "limit": str(limit)}
        raw_json = self._call_api("/metadata", params, None, CallType.GET)

        return parse_obj_as(List[PortfolioMetadata], raw_json["result"])

    def get_portfolio_metadata(self, metadata_id: UUID) -> PortfolioMetadata:
        """
        Get the Portfolio Metadata.

        :param metadata_id: the PortfolioMetadata's unique identity
        :return: `PortfolioMetadata`
        """
        raw_json = self._call_api(f"/metadata/{metadata_id}", {}, None, CallType.GET)
        return PortfolioMetadata.parse_obj(raw_json["result"])

    def update_portfolio_metadata(
        self, metadata_id: UUID, request: PortfolioMetadataUpdateRequest
    ) -> PortfolioMetadata:
        """
        Creates a copy of the Portfolio Metadata and increases the version by 1.

        :param request: the request with all the details needed to update the `PortfolioMetadata`
        :return: the updated `PortfolioMetadata`
        """
        req_json = json.loads(request.json())
        raw_json = self._call_api(
            f"/metadata/{metadata_id}", {}, req_json, CallType.PUT
        )
        return PortfolioMetadata.parse_obj(raw_json["result"])

    def delete_portfolio_metadata(self, metadata_id: UUID):
        """
        Marks the Portfolio Metadata as deleted.

        :param metadata_id: the `PortfolioMetadata` to delete
        """
        self._call_api(f"/metadata/{metadata_id}", {}, None, CallType.DELETE)

    def get_balances_by_metadata_id(
        self, request: PortfolioAccountBalanceRequest
    ) -> List[Balance]:
        """
        Get Balances by account_ids in Portfolio Metadata

        :param request: the request with the `metadata_id`
        :return: a list of `Balance`
        """
        metadata_id = request.metadata_id
        req_json = json.loads(request.json())
        raw_json = self._call_api(
            f"/metadata/{metadata_id}/balances", {}, req_json, CallType.GET
        )
        return parse_obj_as(List[Balance], raw_json["result"])

    def create_portfolio_snapshot(
        self, request: PortfolioSnapshotCreateRequest
    ) -> PortfolioSnapshot:
        """
        Creates a Portfolio Snapshot.

        :param request: the request with the necessary details to create a new `PortfolioSnapshot`
        :return: the created `PortfolioSnapshot`
        """
        req_json = json.loads(request.json())
        raw_json = self._call_api("/snapshots", {}, req_json, CallType.POST)
        return PortfolioSnapshot.parse_obj(raw_json["result"])

    def update_portfolio_snapshot(
        self, snapshot_id: UUID, request: PortfolioSnapshotUpdateRequest
    ) -> PortfolioSnapshot:
        """
        Creates a copy of the Portfolio Snapshot and increases the version by 1.

        :param request: the request with the necessary details to update an `PortfolioSnapshot`
        :return: the updated `PortfolioSnapshot`
        """
        req_json = json.loads(request.json())
        raw_json = self._call_api(
            f"/snapshots/{snapshot_id}", {}, req_json, CallType.PUT
        )
        return PortfolioSnapshot.parse_obj(raw_json["result"])

    def delete_portfolio_snapshot(self, snapshot_id: UUID) -> bool:
        """
        Mark the Portfolio Snapshot as deleted.

        :param snapshot_id: the `PortfolioSnapshot` to delete
        """
        self._call_api(f"/snapshots/{snapshot_id}", {}, None, CallType.DELETE)
        return True

    def list_portfolio_snapshots(
        self, metadata_id: UUID, offset: Optional[int] = 0, limit: Optional[int] = 1000
    ) -> List[PortfolioSnapshot]:
        """
        List all `PortfolioSnapshot` entries that are associated with the given `metadata_id`

        :param metadata_id: the `PortfolioMetadata` id to retrieve the snapshots from.
        :param offset: the number of records to skip in the page.
        :param limit: the maximum number of items that should be returned.
        :return: a list `PortfolioSnapshot`
        """
        params = {"offset": str(offset), "limit": str(limit)}
        raw_json = self._call_api(
            f"/metadata/{metadata_id}/snapshots", params, None, CallType.GET
        )
        return parse_obj_as(List[PortfolioSnapshot], raw_json["result"])

    def get_portfolio_snapshot(self, snapshot_id: UUID) -> PortfolioSnapshot:
        """
        Get the Portfolio Snapshot.

        :param snapshot_id: the PortfolioSnapshot's unique identity
        :return: `PortfolioSnapshot`
        """
        raw_json = self._call_api(f"/snapshots/{snapshot_id}", {}, None, CallType.GET)
        return PortfolioSnapshot.parse_obj(raw_json["result"])

    def to_legacy_portfolio(self, portfolio_snapshot: PortfolioSnapshot) -> Portfolio:
        """
        Convert the `PortfolioSnapshot` to a `Portfolio` type that's compatible with the current SDK Api.

        :param portfolio_snapshot: The `PortfolioSnapshot` to convert
        :return: `Portfolio`
        """
        return Portfolio(
            assets={
                balance.asset_id: balance.quantity
                for balance in portfolio_snapshot.balances
            }
        )
