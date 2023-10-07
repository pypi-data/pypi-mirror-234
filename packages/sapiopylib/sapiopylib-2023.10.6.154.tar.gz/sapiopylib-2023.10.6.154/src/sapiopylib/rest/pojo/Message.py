from __future__ import annotations

import base64
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Any, Dict, List


class SapioMessageFormatException(Exception):
    """
    Thrown when attempting to use the message for delivery, the message is still invalid.
    """
    error: str
    message: Any

    def __init__(self, error: str, message: Any):
        self.error = error
        self.message = message

    def __str__(self):
        return self.error


class EmailAttachmentType(Enum):
    """
    Attachment type inside emails.
    """
    DATA_RECORD = 0
    RAW = 1


class AbstractVeloxEmailAttachment(ABC):
    """
    An attachment that can be included with a VeloxEmailPojo to send email through the Sapio platform.
    """

    @abstractmethod
    def attachment_type(self) -> EmailAttachmentType:
        pass

    def to_json(self) -> Dict[str, Any]:
        return {
            "attachmentType": self.attachment_type().name
        }

    @staticmethod
    def of_raw_email(data: bytes, attachment_name: str):
        return VeloxRawEmailAttachment(data, attachment_name)

    @staticmethod
    def of_record_attachment(data_type_name: str, record_id: int):
        return VeloxDataRecordEmailAttachment(data_type_name, record_id)


class VeloxRawEmailAttachment(AbstractVeloxEmailAttachment):
    """
    An email attachment represented as base 64 encoded bytes.
    """
    data: bytes
    attachment_name: str

    def __init__(self, data: bytes, attachment_name: str):
        self.data = data
        self.attachment_name = attachment_name

    def attachment_type(self) -> EmailAttachmentType:
        return EmailAttachmentType.RAW

    def to_json(self) -> Dict[str, Any]:
        ret = super().to_json()
        b64_data: str = base64.encodebytes(self.data).decode("utf-8")
        ret['bytes'] = b64_data
        ret['attachmentName'] = self.attachment_name
        return ret


class VeloxDataRecordEmailAttachment(AbstractVeloxEmailAttachment):
    """
    An email attachment that is already represented as an attachment record in the Sapio platform.
    When sending an email with this attachment, the platform will look up the attachment data from the attachment
    record and include that data with the email to be sent.
    """
    data_type_name: str
    record_id: int

    def __init__(self, data_type_name: str, record_id: int):
        self.data_type_name = data_type_name
        self.record_id = record_id

    def attachment_type(self) -> EmailAttachmentType:
        return EmailAttachmentType.DATA_RECORD

    def to_json(self) -> Dict[str, Any]:
        ret = super().to_json()
        ret['dataTypeName'] = self.data_type_name
        ret['recordId'] = self.record_id
        return ret


class VeloxEmailRecipient:
    email: str
    name: Optional[str]

    def __init__(self, email: str, name: Optional[str] = None):
        self.email = email
        self.name = name

    def to_json(self) -> Dict[str, Any]:
        return {
            "email": self.email,
            "name": self.name
        }


class VeloxEmail:
    """
    An object representing an email to be sent by the Sapio Platform.
    """
    addr_from: Optional[VeloxEmailRecipient]
    addr_to: List[VeloxEmailRecipient]
    addr_cc: Optional[List[VeloxEmailRecipient]]
    addr_bcc: Optional[List[VeloxEmailRecipient]]
    attachment_list: Optional[List[AbstractVeloxEmailAttachment]]
    subject: str
    plain_text_body: Optional[str]
    html_body: Optional[str]
    headers: Dict[str, str]

    def __init__(self, addr_to: List[VeloxEmailRecipient], subject: str,
                 addr_cc: Optional[List[VeloxEmailRecipient]] = None,
                 addr_bcc: Optional[List[VeloxEmailRecipient]] = None,
                 addr_from: Optional[VeloxEmailRecipient] = None,
                 attachment_list: Optional[List[AbstractVeloxEmailAttachment]] = None,
                 plain_text_body: Optional[str] = None, html_body: Optional[str] = None,
                 headers: Dict[str, str] = None):
        self.addr_from = addr_from
        self.addr_to = addr_to
        self.addr_cc = addr_cc
        self.addr_bcc = addr_bcc
        self.subject = subject
        self.attachment_list = attachment_list
        self.plain_text_body = plain_text_body
        self.html_body = html_body
        self.headers = headers

    def to_json(self) -> Dict[str, Any]:
        if not self.plain_text_body and not self.html_body:
            raise SapioMessageFormatException("Either plain text body or html body must be defined.", self)
        addr_from = None
        if self.addr_from:
            addr_from = self.addr_from.to_json()
        addr_to = None
        if self.addr_to:
            addr_to = [x.to_json() for x in self.addr_to]
        addr_cc = None
        if self.addr_cc:
            addr_cc = [x.to_json() for x in self.addr_cc]
        addr_bcc = None
        if self.addr_bcc:
            addr_bcc = [x.to_json() for x in self.addr_bcc]
        att_list = None
        if self.attachment_list:
            att_list = [x.to_json() for x in self.attachment_list]
        return {
            "from": addr_from,
            "to": addr_to,
            "cc": addr_cc,
            "bcc": addr_bcc,
            "attachmentList": att_list,
            "subject": self.subject,
            "plainTextBody": self.plain_text_body,
            "htmlBody": self.html_body,
            "headers": self.headers
        }


class VeloxMessage:
    """
    An object representing a message to be sent to users within the Sapio Platform.  If no usernames
    or user group names are specified within this object, then the message will be sent to all users within the app.
    """
    usernames: Optional[List[str]]
    group_names: Optional[List[str]]
    message: str

    def __init__(self, message: str, usernames: Optional[List[str]] = None, group_names: Optional[List[str]] = None):
        self.usernames = usernames
        self.group_names = group_names
        self.message = message

    def to_json(self) -> Dict[str, Any]:
        return {
            "usernameSet": self.usernames,
            "userGroupNameSet": self.group_names,
            "message": self.message
        }

    @staticmethod
    def broadcast_message(message: str):
        return VeloxMessage(message)

    @staticmethod
    def user_message(usernames: List[str], message: str):
        return VeloxMessage(message, usernames=usernames)

    @staticmethod
    def group_message(group_names: List[str], message: str):
        return VeloxMessage(message, group_names=group_names)
