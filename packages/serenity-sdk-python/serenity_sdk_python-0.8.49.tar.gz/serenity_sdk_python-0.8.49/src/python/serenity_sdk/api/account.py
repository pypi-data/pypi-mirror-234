import json
from typing import List, Optional
from uuid import UUID

from pydantic import parse_obj_as
from serenity_sdk.api.core import SerenityApi
from serenity_sdk.client.raw import CallType, SerenityClient
from serenity_types.account.core import (Account,
                                         AccountCreationRequest,
                                         AccountUpdateRequest,
                                         SourcePlatform)


class AccountApi(SerenityApi):
    def __init__(self, client: SerenityClient):
        """
        :param client: the raw client to delegate to when making API calls
        """
        super().__init__(client, 'org/accounts')

    def create_account(self, request: AccountCreationRequest) -> Account:
        """
        Creates a new Portfolio Metadata.

        :param request: the request with the necessary details to create a new `Account`
        :return: the created `Account`
        """
        req_json = json.loads(request.json())
        raw_json = self._call_api('/', {}, req_json, CallType.POST)
        return Account.parse_obj(raw_json['result'])

    def list_supported_source_platforms(self) -> List[SourcePlatform]:
        """
        List all SourcePlatforms that support automatic portfolio syncing.

        :return: a list `SourcePlatform`
        """
        raw_json = self._call_api('/source-platforms', {}, None, CallType.GET)
        return parse_obj_as(List[SourcePlatform], raw_json['result'])

    def update_account(self, account_id: str, request: AccountUpdateRequest) -> Account:
        """
        Update the account based on account_id. Will fail if account has been deleted.

        :param request: the request with the necessary details to update an `Account`
        :return: the updated `Account`
        """
        req_json = json.loads(request.json())
        raw_json = self._call_api(f'/{account_id}', {}, req_json, CallType.PUT)
        return Account.parse_obj(raw_json['result'])

    def list_accounts(self, offset: Optional[int] = 0, limit: Optional[int] = 1000) -> List[Account]:
        """
        List all `Account` not marked as deleted in the Organization

        :param offset: the number of records to skip in the page.
        :param limit: the maximum number of items that should be returned.
        :return: a list `Account`
        """
        params = {
            "offset": offset,
            "limit": limit
        }
        raw_json = self._call_api('/', params, None, CallType.GET)
        return parse_obj_as(List[Account], raw_json['result'])

    def retrieve_accounts_batch(self, account_ids: List[UUID]) -> List[Account]:
        """
        Retrieve the accounts based on account_ids. Will fail if any account has been deleted.

        :param account_ids: account ids to retrieve
        :return: A list of Accounts
        """
        params = {
            "account_ids": account_ids
        }
        raw_json = self._call_api('/batch', params, None, CallType.GET)
        return parse_obj_as(List[Account], raw_json['result'])

    def get_account(self, account_id: UUID) -> Account:
        """
        Retrieve the account based on account_id. Will fail if account has been deleted.

        :param account_id: the account id to retrieve
        :return: the `Account` based on the `account_id`
        """
        raw_json = self._call_api(f'/{account_id}', {}, None, CallType.GET)
        return Account.parse_obj(raw_json['result'])

    def delete_account(self, account_id: UUID):
        """
        Delete Account

        :param account_id: the account id to delete
        """
        self._call_api(f'/{account_id}', {}, None, CallType.DELETE)
