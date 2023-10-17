# This file was automatically generated. DO NOT EDIT.
# If you have any remark or suggestion do not hesitate to open an issue.
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

from scaleway_core.bridge import (
    Region,
)
from scaleway_core.utils import (
    StrEnumMeta,
)


class DomainLastStatusRecordStatus(str, Enum, metaclass=StrEnumMeta):
    UNKNOWN_RECORD_STATUS = "unknown_record_status"
    VALID = "valid"
    INVALID = "invalid"
    NOT_FOUND = "not_found"

    def __str__(self) -> str:
        return str(self.value)


class DomainStatus(str, Enum, metaclass=StrEnumMeta):
    UNKNOWN = "unknown"
    CHECKED = "checked"
    UNCHECKED = "unchecked"
    INVALID = "invalid"
    LOCKED = "locked"
    REVOKED = "revoked"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)


class EmailFlag(str, Enum, metaclass=StrEnumMeta):
    UNKNOWN_FLAG = "unknown_flag"
    SOFT_BOUNCE = "soft_bounce"
    HARD_BOUNCE = "hard_bounce"
    SPAM = "spam"
    MAILBOX_FULL = "mailbox_full"
    MAILBOX_NOT_FOUND = "mailbox_not_found"
    GREYLISTED = "greylisted"
    SEND_BEFORE_EXPIRATION = "send_before_expiration"

    def __str__(self) -> str:
        return str(self.value)


class EmailRcptType(str, Enum, metaclass=StrEnumMeta):
    UNKNOWN_RCPT_TYPE = "unknown_rcpt_type"
    TO = "to"
    CC = "cc"
    BCC = "bcc"

    def __str__(self) -> str:
        return str(self.value)


class EmailStatus(str, Enum, metaclass=StrEnumMeta):
    UNKNOWN = "unknown"
    NEW = "new"
    SENDING = "sending"
    SENT = "sent"
    FAILED = "failed"
    CANCELED = "canceled"

    def __str__(self) -> str:
        return str(self.value)


class ListEmailsRequestOrderBy(str, Enum, metaclass=StrEnumMeta):
    CREATED_AT_DESC = "created_at_desc"
    CREATED_AT_ASC = "created_at_asc"
    UPDATED_AT_DESC = "updated_at_desc"
    UPDATED_AT_ASC = "updated_at_asc"
    STATUS_DESC = "status_desc"
    STATUS_ASC = "status_asc"
    MAIL_FROM_DESC = "mail_from_desc"
    MAIL_FROM_ASC = "mail_from_asc"
    MAIL_RCPT_DESC = "mail_rcpt_desc"
    MAIL_RCPT_ASC = "mail_rcpt_asc"
    SUBJECT_DESC = "subject_desc"
    SUBJECT_ASC = "subject_asc"

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class EmailTry:
    message: str
    """
    The SMTP message received. If the attempt did not reach an SMTP server, the message returned explains what happened.
    """

    code: int
    """
    The SMTP status code received after the attempt. 0 if the attempt did not reach an SMTP server.
    """

    rank: int
    """
    Rank number of this attempt to send the email.
    """

    tried_at: Optional[datetime]
    """
    Date of the attempt to send the email.
    """


@dataclass
class DomainStatistics:
    canceled_count: int

    failed_count: int

    sent_count: int

    total_count: int


@dataclass
class CreateEmailRequestAddress:
    email: str
    """
    Email address.
    """

    name: Optional[str]
    """
    (Optional) Name displayed.
    """


@dataclass
class CreateEmailRequestAttachment:
    content: str
    """
    Content of the attachment encoded in base64.
    """

    type_: str
    """
    MIME type of the attachment.
    """

    name: str
    """
    Filename of the attachment.
    """


@dataclass
class Email:
    try_count: int
    """
    Number of attempts to send the email.
    """

    last_tries: List[EmailTry]
    """
    Information about the last three attempts to send the email.
    """

    subject: str
    """
    Subject of the email.
    """

    id: str
    """
    Technical ID of the email.
    """

    mail_rcpt: str
    """
    Email address of the recipient.
    """

    flags: List[EmailFlag]
    """
    Flags categorize emails. They allow you to obtain more information about recurring errors, for example.
    """

    mail_from: str
    """
    Email address of the sender.
    """

    project_id: str
    """
    ID of the Project to which the email belongs.
    """

    message_id: str
    """
    Message ID of the email.
    """

    status: EmailStatus
    """
    Status of the email.
    """

    rcpt_type: EmailRcptType
    """
    Type of recipient.
    """

    status_details: Optional[str]
    """
    Additional status information.
    """

    updated_at: Optional[datetime]
    """
    Last update of the email object.
    """

    created_at: Optional[datetime]
    """
    Creation date of the email object.
    """

    rcpt_to: Optional[str]
    """
    Email address of the recipient.
    """


@dataclass
class DomainLastStatusDkimRecord:
    status: DomainLastStatusRecordStatus
    """
    Status of the DKIM record's configurartion.
    """

    last_valid_at: Optional[datetime]
    """
    Time and date the DKIM record was last valid.
    """

    error: Optional[str]
    """
    An error text displays in case the record is not valid.
    """


@dataclass
class DomainLastStatusSpfRecord:
    status: DomainLastStatusRecordStatus
    """
    Status of the SPF record's configurartion.
    """

    last_valid_at: Optional[datetime]
    """
    Time and date the SPF record was last valid.
    """

    error: Optional[str]
    """
    An error text displays in case the record is not valid.
    """


@dataclass
class Domain:
    dkim_config: str
    """
    DKIM public key to record in the DNS zone.
    """

    statistics: DomainStatistics
    """
    Domain's statistics.
    """

    id: str
    """
    ID of the domain.
    """

    region: Region
    """
    Region to target. If none is passed will use default region from the config.
    """

    status: DomainStatus
    """
    Status of the domain.
    """

    name: str
    """
    Domain name (example.com).
    """

    project_id: str
    """
    ID of the domain's Project.
    """

    organization_id: str
    """
    ID of the domain's Organization.
    """

    spf_config: str
    """
    Snippet of the SPF record to register in the DNS zone.
    """

    next_check_at: Optional[datetime]
    """
    Date and time of the next scheduled check.
    """

    last_error: Optional[str]
    """
    Error message returned if the last check failed.
    """

    revoked_at: Optional[datetime]
    """
    Date and time of the domain's deletion.
    """

    last_valid_at: Optional[datetime]
    """
    Date and time the domain was last valid.
    """

    created_at: Optional[datetime]
    """
    Date and time of domain creation.
    """


@dataclass
class CancelEmailRequest:
    email_id: str
    """
    ID of the email to cancel.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """


@dataclass
class CheckDomainRequest:
    domain_id: str
    """
    ID of the domain to check.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """


@dataclass
class CreateDomainRequest:
    accept_tos: bool
    """
    Accept Scaleway's Terms of Service.
    """

    domain_name: str
    """
    Fully qualified domain dame.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    project_id: Optional[str]
    """
    ID of the project to which the domain belongs.
    """


@dataclass
class CreateEmailRequest:
    html: str
    """
    HTML content.
    """

    text: str
    """
    Text content.
    """

    subject: str
    """
    Subject of the email.
    """

    from_: CreateEmailRequestAddress
    """
    Sender information. Must be from a checked domain declared in the Project.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    to: Optional[List[CreateEmailRequestAddress]]
    """
    An array of the primary recipient's information.
    """

    cc: Optional[List[CreateEmailRequestAddress]]
    """
    An array of the carbon copy recipient's information.
    """

    bcc: Optional[List[CreateEmailRequestAddress]]
    """
    An array of the blind carbon copy recipient's information.
    """

    project_id: Optional[str]
    """
    ID of the Project in which to create the email.
    """

    attachments: Optional[List[CreateEmailRequestAttachment]]
    """
    Array of attachments.
    """

    send_before: Optional[datetime]
    """
    Maximum date to deliver the email.
    """


@dataclass
class CreateEmailResponse:
    emails: List[Email]
    """
    Single page of emails matching the requested criteria.
    """


@dataclass
class DomainLastStatus:
    dkim_record: DomainLastStatusDkimRecord
    """
    The DKIM record verification data.
    """

    spf_record: DomainLastStatusSpfRecord
    """
    The SPF record verification data.
    """

    domain_name: str
    """
    The domain name (example.com).
    """

    domain_id: str
    """
    The id of the domain.
    """


@dataclass
class GetDomainLastStatusRequest:
    domain_id: str
    """
    ID of the domain to delete.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """


@dataclass
class GetDomainRequest:
    domain_id: str
    """
    ID of the domain.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """


@dataclass
class GetEmailRequest:
    email_id: str
    """
    ID of the email to retrieve.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """


@dataclass
class GetStatisticsRequest:
    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    project_id: Optional[str]
    """
    (Optional) Number of emails for this Project.
    """

    domain_id: Optional[str]
    """
    (Optional) Number of emails sent from this domain (must be coherent with the `project_id` and the `organization_id`).
    """

    since: Optional[datetime]
    """
    (Optional) Number of emails created after this date.
    """

    until: Optional[datetime]
    """
    (Optional) Number of emails created before this date.
    """

    mail_from: Optional[str]
    """
    (Optional) Number of emails sent with this sender's email address.
    """


@dataclass
class ListDomainsRequest:
    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    page: Optional[int]
    """
    Requested page number. Value must be greater or equal to 1.
    """

    page_size: Optional[int]
    """
    Page size.
    """

    project_id: Optional[str]

    status: Optional[List[DomainStatus]]

    organization_id: Optional[str]

    name: Optional[str]


@dataclass
class ListDomainsResponse:
    domains: List[Domain]

    total_count: int
    """
    Number of domains that match the request (without pagination).
    """


@dataclass
class ListEmailsRequest:
    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """

    page: Optional[int]

    page_size: Optional[int]

    project_id: Optional[str]
    """
    (Optional) ID of the Project in which to list the emails.
    """

    domain_id: Optional[str]
    """
    (Optional) ID of the domain for which to list the emails.
    """

    message_id: Optional[str]
    """
    (Optional) ID of the message for which to list the emails.
    """

    since: Optional[datetime]
    """
    (Optional) List emails created after this date.
    """

    until: Optional[datetime]
    """
    (Optional) List emails created before this date.
    """

    mail_from: Optional[str]
    """
    (Optional) List emails sent with this sender's email address.
    """

    mail_to: Optional[str]
    """
    List emails sent to this recipient's email address.
    """

    mail_rcpt: Optional[str]
    """
    (Optional) List emails sent to this recipient's email address.
    """

    statuses: Optional[List[EmailStatus]]
    """
    (Optional) List emails with any of these statuses.
    """

    subject: Optional[str]
    """
    (Optional) List emails with this subject.
    """

    search: Optional[str]
    """
    (Optional) List emails by searching to all fields.
    """

    order_by: Optional[ListEmailsRequestOrderBy]
    """
    (Optional) List emails corresponding to specific criteria.
    """

    flags: Optional[List[EmailFlag]]
    """
    (Optional) List emails containing only specific flags.
    """


@dataclass
class ListEmailsResponse:
    emails: List[Email]
    """
    Single page of emails matching the requested criteria.
    """

    total_count: int
    """
    Number of emails matching the requested criteria.
    """


@dataclass
class RevokeDomainRequest:
    domain_id: str
    """
    ID of the domain to delete.
    """

    region: Optional[Region]
    """
    Region to target. If none is passed will use default region from the config.
    """


@dataclass
class Statistics:
    canceled_count: int
    """
    Number of emails in the final `canceled` state. This means emails that have been canceled upon request.
    """

    failed_count: int
    """
    Number of emails in the final `failed` state. This means emails that have been refused by the target mail system with a final error status.
    """

    sent_count: int
    """
    Number of emails in the final `sent` state. This means emails that have been delivered to the target mail system.
    """

    sending_count: int
    """
    Number of emails still in the `sending` transient state. This means emails received from the API but not yet in their final status.
    """

    new_count: int
    """
    Number of emails still in the `new` transient state. This means emails received from the API but not yet processed.
    """

    total_count: int
    """
    Total number of emails matching the requested criteria.
    """
