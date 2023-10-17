# This file was automatically generated. DO NOT EDIT.
# If you have any remark or suggestion do not hesitate to open an issue.
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

from scaleway_core.bridge import (
    TimeSeries,
)
from scaleway_core.utils import (
    StrEnumMeta,
)


class CockpitStatus(str, Enum, metaclass=StrEnumMeta):
    UNKNOWN_STATUS = "unknown_status"
    CREATING = "creating"
    READY = "ready"
    DELETING = "deleting"
    UPDATING = "updating"
    ERROR = "error"

    def __str__(self) -> str:
        return str(self.value)


class DatasourceType(str, Enum, metaclass=StrEnumMeta):
    UNKNOWN_DATASOURCE_TYPE = "unknown_datasource_type"
    METRICS = "metrics"
    LOGS = "logs"
    TRACES = "traces"
    ALERTS = "alerts"

    def __str__(self) -> str:
        return str(self.value)


class GrafanaUserRole(str, Enum, metaclass=StrEnumMeta):
    UNKNOWN_ROLE = "unknown_role"
    EDITOR = "editor"
    VIEWER = "viewer"

    def __str__(self) -> str:
        return str(self.value)


class ListDatasourcesRequestOrderBy(str, Enum, metaclass=StrEnumMeta):
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"

    def __str__(self) -> str:
        return str(self.value)


class ListGrafanaUsersRequestOrderBy(str, Enum, metaclass=StrEnumMeta):
    LOGIN_ASC = "login_asc"
    LOGIN_DESC = "login_desc"

    def __str__(self) -> str:
        return str(self.value)


class ListPlansRequestOrderBy(str, Enum, metaclass=StrEnumMeta):
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"

    def __str__(self) -> str:
        return str(self.value)


class ListTokensRequestOrderBy(str, Enum, metaclass=StrEnumMeta):
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"

    def __str__(self) -> str:
        return str(self.value)


class PlanName(str, Enum, metaclass=StrEnumMeta):
    UNKNOWN_NAME = "unknown_name"
    FREE = "free"
    PREMIUM = "premium"
    CUSTOM = "custom"

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class ContactPointEmail:
    to: str


@dataclass
class TokenScopes:
    write_traces: bool
    """
    Permission to write traces.
    """

    query_traces: bool
    """
    Permission to fetch traces.
    """

    setup_alerts: bool
    """
    Permission to set up alerts.
    """

    setup_logs_rules: bool
    """
    Permission to set up logs rules.
    """

    write_logs: bool
    """
    Permission to write logs.
    """

    query_logs: bool
    """
    Permission to fetch logs.
    """

    setup_metrics_rules: bool
    """
    Permission to setup metrics rules.
    """

    write_metrics: bool
    """
    Permission to write metrics.
    """

    query_metrics: bool
    """
    Permission to fetch metrics.
    """


@dataclass
class CockpitEndpoints:
    grafana_url: str
    """
    URL for the Grafana dashboard.
    """

    alertmanager_url: str
    """
    URL for the alert manager.
    """

    logs_url: str
    """
    URL for logs.
    """

    metrics_url: str
    """
    URL for metrics.
    """


@dataclass
class Plan:
    """
    Pricing plan.
    """

    retention_price: int
    """
    Retention price in euros per month.
    """

    logs_ingestion_price: int
    """
    Ingestion price for 1 GB of logs in cents.
    """

    sample_ingestion_price: int
    """
    Ingestion price for 1 million samples in cents.
    """

    name: PlanName
    """
    Name of a given pricing plan.
    """

    id: str
    """
    ID of a given pricing plan.
    """

    retention_metrics_interval: Optional[str]
    """
    Retention for metrics.
    """

    retention_logs_interval: Optional[str]
    """
    Retention for logs.
    """


@dataclass
class ContactPoint:
    """
    Contact point.
    """

    email: Optional[ContactPointEmail]


@dataclass
class Datasource:
    """
    Datasource.
    """

    type_: DatasourceType
    """
    Datasource type.
    """

    url: str
    """
    Datasource URL.
    """

    name: str
    """
    Datasource name.
    """

    project_id: str
    """
    ID of the Project the Cockpit belongs to.
    """

    id: str
    """
    ID of the datasource.
    """


@dataclass
class GrafanaUser:
    """
    Grafana user.
    """

    role: GrafanaUserRole
    """
    Role assigned to the Grafana user.
    """

    login: str
    """
    Username of the Grafana user.
    """

    id: int
    """
    ID of the Grafana user.
    """

    password: Optional[str]
    """
    The Grafana user's password.
    """


@dataclass
class Token:
    scopes: TokenScopes
    """
    Token's permissions.
    """

    name: str
    """
    Name of the token.
    """

    project_id: str
    """
    ID of the Project.
    """

    id: str
    """
    ID of the token.
    """

    created_at: Optional[datetime]
    """
    Date and time of the token's creation.
    """

    updated_at: Optional[datetime]
    """
    Date and time of the token's last update.
    """

    secret_key: Optional[str]
    """
    Token's secret key.
    """


@dataclass
class ActivateCockpitRequest:
    project_id: Optional[str]
    """
    ID of the Project the Cockpit belongs to.
    """


@dataclass
class Cockpit:
    """
    Cockpit.
    """

    plan: Plan
    """
    Pricing plan information.
    """

    managed_alerts_enabled: bool
    """
    Specifies whether managed alerts are enabled or disabled.
    """

    status: CockpitStatus
    """
    Status of the Cockpit.
    """

    endpoints: CockpitEndpoints
    """
    Endpoints of the Cockpit.
    """

    project_id: str
    """
    ID of the Project the Cockpit belongs to.
    """

    created_at: Optional[datetime]
    """
    Date and time of the Cockpit's creation.
    """

    updated_at: Optional[datetime]
    """
    Date and time of the Cockpit's last update.
    """


@dataclass
class CockpitMetrics:
    """
    Metrics for a given Cockpit.
    """

    timeseries: List[TimeSeries]
    """
    Time series array.
    """


@dataclass
class CreateContactPointRequest:
    """
    Request to create a contact point.
    """

    project_id: Optional[str]
    """
    ID of the Project in which to create the contact point.
    """

    contact_point: Optional[ContactPoint]
    """
    Contact point to create.
    """


@dataclass
class CreateDatasourceRequest:
    """
    Request to create a datasource.
    """

    name: str
    """
    Datasource name.
    """

    project_id: Optional[str]
    """
    ID of the Project the Cockpit belongs to.
    """

    type_: Optional[DatasourceType]
    """
    Datasource type.
    """


@dataclass
class CreateGrafanaUserRequest:
    """
    Request to create a Grafana user.
    """

    login: str
    """
    Username of the Grafana user.
    """

    project_id: Optional[str]
    """
    ID of the Project.
    """

    role: Optional[GrafanaUserRole]
    """
    Role assigned to the Grafana user.
    """


@dataclass
class CreateTokenRequest:
    scopes: TokenScopes
    """
    Token's permissions.
    """

    project_id: Optional[str]
    """
    ID of the Project.
    """

    name: Optional[str]
    """
    Name of the token.
    """


@dataclass
class DeactivateCockpitRequest:
    project_id: Optional[str]
    """
    ID of the Project the Cockpit belongs to.
    """


@dataclass
class DeleteContactPointRequest:
    """
    Request to delete a contact point.
    """

    project_id: Optional[str]
    """
    ID of the Project.
    """

    contact_point: Optional[ContactPoint]
    """
    Contact point to delete.
    """


@dataclass
class DeleteGrafanaUserRequest:
    """
    Request to delete a Grafana user.
    """

    grafana_user_id: int
    """
    ID of the Grafana user.
    """

    project_id: Optional[str]
    """
    ID of the Project.
    """


@dataclass
class DeleteTokenRequest:
    token_id: str
    """
    ID of the token.
    """


@dataclass
class DisableManagedAlertsRequest:
    """
    Request to disable the sending of managed alerts.
    """

    project_id: Optional[str]
    """
    ID of the Project.
    """


@dataclass
class EnableManagedAlertsRequest:
    """
    Request to enable the sending of managed alerts.
    """

    project_id: Optional[str]
    """
    ID of the Project.
    """


@dataclass
class GetCockpitMetricsRequest:
    """
    Request to get a given Cockpit's metrics.
    """

    project_id: Optional[str]
    """
    ID of the Project the Cockpit belongs to.
    """

    start_date: Optional[datetime]
    """
    Desired time range's start date for the metrics.
    """

    end_date: Optional[datetime]
    """
    Desired time range's end date for the metrics.
    """

    metric_name: Optional[str]
    """
    Name of the metric requested.
    """


@dataclass
class GetCockpitRequest:
    project_id: Optional[str]
    """
    ID of the Project the Cockpit belongs to.
    """


@dataclass
class GetTokenRequest:
    token_id: str
    """
    ID of the token.
    """


@dataclass
class ListContactPointsRequest:
    """
    Request to list all contact points.
    """

    page: Optional[int]
    """
    Page number.
    """

    page_size: Optional[int]
    """
    Page size.
    """

    project_id: Optional[str]
    """
    ID of the Project from which to list the contact points.
    """


@dataclass
class ListContactPointsResponse:
    """
    Response returned when listing contact points.
    """

    has_additional_contact_points: bool
    """
    Specifies whether there are unmanaged contact points.
    """

    has_additional_receivers: bool
    """
    Specifies whether the contact point has other receivers than the default receiver.
    """

    contact_points: List[ContactPoint]
    """
    Array of contact points.
    """

    total_count: int
    """
    Count of all contact points created.
    """


@dataclass
class ListDatasourcesRequest:
    page: Optional[int]
    """
    Page number.
    """

    page_size: Optional[int]
    """
    Page size.
    """

    order_by: Optional[ListDatasourcesRequestOrderBy]
    """
    How the response is ordered.
    """

    project_id: Optional[str]
    """
    ID of the Project.
    """

    types: Optional[List[DatasourceType]]
    """
    Filter by datasource types.
    """


@dataclass
class ListDatasourcesResponse:
    datasources: List[Datasource]
    """
    List of the datasources within the pagination.
    """

    total_count: int
    """
    Count of all datasources corresponding to the request.
    """


@dataclass
class ListGrafanaUsersRequest:
    """
    Request to list all Grafana users.
    """

    page: Optional[int]
    """
    Page number.
    """

    page_size: Optional[int]
    """
    Page size.
    """

    order_by: Optional[ListGrafanaUsersRequestOrderBy]

    project_id: Optional[str]
    """
    ID of the Project.
    """


@dataclass
class ListGrafanaUsersResponse:
    """
    Response returned when listing Grafana users.
    """

    grafana_users: List[GrafanaUser]
    """
    Information on all Grafana users.
    """

    total_count: int
    """
    Count of all Grafana users.
    """


@dataclass
class ListPlansRequest:
    """
    Request to list all pricing plans.
    """

    page: Optional[int]
    """
    Page number.
    """

    page_size: Optional[int]
    """
    Page size.
    """

    order_by: Optional[ListPlansRequestOrderBy]


@dataclass
class ListPlansResponse:
    """
    Response returned when listing all pricing plans.
    """

    plans: List[Plan]
    """
    Information on plans.
    """

    total_count: int
    """
    Count of all pricing plans.
    """


@dataclass
class ListTokensRequest:
    page: Optional[int]
    """
    Page number.
    """

    page_size: Optional[int]
    """
    Page size.
    """

    order_by: Optional[ListTokensRequestOrderBy]
    """
    How the response is ordered.
    """

    project_id: Optional[str]
    """
    ID of the Project.
    """


@dataclass
class ListTokensResponse:
    tokens: List[Token]
    """
    List of all tokens created.
    """

    total_count: int
    """
    Count of all tokens created.
    """


@dataclass
class ResetCockpitGrafanaRequest:
    project_id: Optional[str]
    """
    ID of the Project the Cockpit belongs to.
    """


@dataclass
class ResetGrafanaUserPasswordRequest:
    """
    Request to reset a Grafana user's password.
    """

    grafana_user_id: int
    """
    ID of the Grafana user.
    """

    project_id: Optional[str]
    """
    ID of the Project.
    """


@dataclass
class SelectPlanRequest:
    """
    Request to select a specific pricing plan.
    """

    plan_id: str
    """
    ID of the pricing plan.
    """

    project_id: Optional[str]
    """
    ID of the Project.
    """


@dataclass
class SelectPlanResponse:
    """
    Response returned when selecting a pricing plan.
    """

    pass


@dataclass
class TriggerTestAlertRequest:
    project_id: Optional[str]
