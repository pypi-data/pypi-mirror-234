from datetime import datetime
from enum import Enum
from typing import List, Optional, Union
from uuid import UUID
from pydantic import validator

from serenity_types.utils.serialization import CamelModel
from serenity_types.pricing.core import MarkTime
from serenity_types.valuation.core import (
    AssetWeight, PortfolioTimeseriesFrequency, RebalancingFrequency,
    PortfolioComposition, CustomizedPortfolioComposition
)


class BenchmarkType(Enum):
    """
    Simple classification of the type of benchmark, reflective
    of its origin and who maintains it.
    """

    PREDEFINED = "PREDEFINED"
    """
    A benchmark offered as part of Serenity, owned and maintained
    by the Cloudwall Research team.
    """

    PRELOADED = "PRELOADED"
    """
    A benchmark offered by a third party vendor like MSCI or S&P.
    """

    CUSTOM = "CUSTOM"
    """
    A benchmark created by the client themselves and stored on the server.
    """

    TRANSIENT = "TRANSIENT"
    """
    A benchmark provided as input ot analytics with zero information
    about where it came from, methodology, etc.. In V1 this is the *only*
    type of benchmark we need to support, with minimal metadata.
    """


class CustomBenchmarkAutoRebalancingDefinition(CamelModel):
    """
    Custom benchmark with auto rebalancing feature definition.
    From an initial cash positions and a set of weights and a rebalancing rule,
    the server then generates a series of positions at a given frequency, e.g. daily, rebalancing
    periodically to bring the positions in line with the desired weights.
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
    The timestamp of which the generated benchmark snapshot should start from.
    """

    end_datetime: Optional[datetime] = None
    """
    The timestamp of which the generated benchmark snapshot should end.
    Defaults to None which denotes generated benchmark snapshot to always have latest date position.
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


class BenchmarkMetadata(CamelModel):
    """
    Metadata describing a particular benchmark offering.
    """

    metadata_id: UUID
    """
    Serenity's unique ID for this benchmark metadata.
    """

    benchmark_type: BenchmarkType
    """
    Classification for this benchmark.
    """

    effective_datetime: datetime
    """
    The effective datetime for this benchmark metadata.
    """

    updated_at: datetime
    """
    Last update timestamp, in UTC.
    """

    updated_by: Optional[str] = None
    """
    Last update user.
    """

    owner: Optional[str] = None
    """
    The primary owner of this benchmark.
    """

    base_currency_id: UUID
    """
    The accounting currency to use for valuation, reporting, etc., e.g. fund reports in USD.
    """

    symbol: Optional[str] = None
    """
    Conventional symbol used for this index, e.g. MVDA.
    """

    display_name: Optional[str] = None
    """
    Short human-readable name for this index, e.g. MarketVector Digital Assets 100. Required
    for CUSTOM, PRELOADED, PREDEFINED.
    """

    description: Optional[str] = None
    """
    Longer human-readable description of this index and its essential methodology. Required
    for CUSTOM, PRELOADED, PREDEFINED.
    """

    provider_id: Optional[UUID] = None
    """
    Organization ID from Serenity's database. Optional unless PRELOADED.
    """

    index_family: Optional[str] = None
    """
    Grouping that this benchmark index belongs to; typically used for PRELOADED, for vendors.
    """

    license_required: bool = False
    """
    Does the client require a license for the index in order to use it? Only applies to PRELOADED.
    """

    license_contact: Optional[str] = None
    """
    If client not licensed, who should they be prompted to contact? Only applies to PRELOADED.
    """

    auto_rebalancing: bool = False
    """
    Flag to indicate if Serenity should do auto rebalancing for the specified CUSTOM benchmark.

    If set to True, Serenity will automatically generated the benchmark snapshots based on
    auto_rebalancing_definition and users are not allowed to manually create/update snapshots
    for this benchmark metadata.
    """

    auto_rebalancing_definition: Optional[CustomBenchmarkAutoRebalancingDefinition] = None
    """
    Custom benchmark auto rebalancing definition.
    Optional unless CUSTOM and auto_rebalancing is set to True.
    """


class CustomBenchmarkMetadataRequest(CamelModel):
    """
    Input for creating/updating custom benchmark metadata.
    """

    display_name: str
    """
    Short human-readable name for this index, e.g. MarketVector Digital Assets 100.
    """

    description: str
    """
    Longer human-readable description of this index and its essential methodology.
    """

    effective_datetime: Optional[datetime] = None
    """
    The effective datetime for this benchmark metadata.
    If not specified, defaults to current datetime.
    """

    updated_by: Optional[str] = None
    """
    Last update user.
    """

    owner: Optional[str] = None
    """
    The primary owner of this benchmark.
    """

    symbol: Optional[str] = None
    """
    Conventional symbol used for this index, e.g. MVDA.
    """

    base_currency_id: Optional[UUID] = None
    """
    The accounting currency to use for valuation, reporting, etc., e.g. fund reports in USD.
    Defaults to `USD` if it's not provided.
    """

    auto_rebalancing: bool = False
    """
    Flag to indicate if Serenity should do auto rebalancing for the specified CUSTOM benchmark.
    """

    auto_rebalancing_definition: Optional[CustomBenchmarkAutoRebalancingDefinition] = None
    """
    Custom benchmark auto rebalancing definition. Optional unless auto_rebalancing is set to True.
    """


class BenchmarkSnapshot(CamelModel):
    """
    Snapshot of the positions of a benchmark at a specific point in time.
    """

    snapshot_id: UUID
    """
    Unique and immutable ID.
    """

    benchmark_metadata: BenchmarkMetadata
    """
    The benchmark metadata that this benchmark snapshot is part of.
    """

    effective_datetime: datetime
    """
    The effective datetime for this benchmark snapshot.
    """

    updated_at: datetime
    """
    Last update timestamp, in UTC.
    """

    updated_by: Optional[str] = None
    """
    Last update user.
    """

    composition_history: Union[PortfolioComposition, CustomizedPortfolioComposition]
    """
    The benchmark snapshot composition history.
    """


class CustomBenchmarkSnapshotRequest(CamelModel):

    effective_datetime: datetime = datetime.utcnow()
    """
    The effective datetime for this benchmark metadata.
    If not specified, defaults to current datetime.
    """

    updated_by: Optional[str] = None
    """
    Last update user.
    """

    composition_history: Union[PortfolioComposition, CustomizedPortfolioComposition]
    """
    The history of index holdings.
    """


class CreateCustomBenchmarkSnapshotRequest(CustomBenchmarkSnapshotRequest):

    metadata_id: UUID
    """
    Serenity's unique ID for the benchmark metadata.
    """


class UpdateCustomBenchmarkSnapshotRequest(CustomBenchmarkSnapshotRequest):
    pass
