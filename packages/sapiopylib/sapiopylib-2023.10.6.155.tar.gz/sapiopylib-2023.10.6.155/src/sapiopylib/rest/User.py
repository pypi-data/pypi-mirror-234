from __future__ import annotations
import sys
import urllib.parse
from base64 import b64encode
from typing import Optional, Callable, List, Dict, Any

import requests
from requests import Response
from typing.io import IO
import logging


class UserSessionAdditionalData:
    """
    The session info for the current session. This is not necessary to establish connection from client to server,
    but can provide useful info for a webservice user program.
    """
    current_group_id: Optional[int]
    current_group_name: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    utc_offset_seconds: int

    def __init__(self, current_group_id: Optional[int], current_group_name: Optional[str],
                 first_name: Optional[str], middle_name: Optional[str], last_name: Optional[str], email: Optional[str],
                 utc_offset_seconds: int):
        self.current_group_id = current_group_id
        self.current_group_name = current_group_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.utc_offset_seconds = utc_offset_seconds


def parse_session_additional_data(json_dct: Dict[str, Any]) -> UserSessionAdditionalData:
    current_group_id: Optional[int] = json_dct.get('currentGroupId')
    current_group_name: Optional[str] = json_dct.get('currentGroupName')
    first_name: Optional[str] = json_dct.get('firstName')
    middle_name: Optional[str] = json_dct.get('middleName')
    last_name: Optional[str] = json_dct.get('lastName')
    email: Optional[str] = json_dct.get('email')
    utc_offset_seconds: int = json_dct.get('utcOffsetSeconds')
    return UserSessionAdditionalData(current_group_id=current_group_id, current_group_name=current_group_name,
                                     first_name=first_name, middle_name=middle_name, last_name=last_name,
                                     email=email, utc_offset_seconds=utc_offset_seconds)


class SapioServerException(Exception):
    """
    This will be thrown when the client cannot perform an operation.
    """
    client_error: requests.exceptions.HTTPError

    def __init__(self, client_error: requests.exceptions.HTTPError):
        self.client_error = client_error

    def __str__(self):
        if self.client_error.response is None or not hasattr(self.client_error.response, "status_code"):
            return "The remote host has not returned any response."
        status_code: int = self.client_error.response.status_code
        message: Optional[str] = ""
        if hasattr(self.client_error.response, "text"):
            message = self.client_error.response.text
        ret: str = "[" + str(status_code) + "]"
        if message:
            ret += ": " + message
        return ret


def ensure_logger_initialized(logger: logging.Logger):
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)


class SapioUser:
    """
    The Sapio REST API Client stores the REST connection info for each new requests.
    There are two main ways to authenticate, with API token, and with username/password.
    """
    url: str
    api_token: Optional[str]
    username: Optional[str]
    password: Optional[str]
    guid: Optional[str]
    account_name: Optional[str]
    verify_ssl_cert: bool
    timeout_seconds: int
    __next_temp_record_id: int
    logger: logging.Logger

    _session_additional_data: Optional[UserSessionAdditionalData]

    def __init__(self, url: str,
                 verify_ssl_cert: bool = True, timeout_seconds: int = 60,
                 api_token: str = None, username: str = None, password: str = None,
                 guid: str = None, account_name: str = None,
                 session_additional_data: Optional[UserSessionAdditionalData] = None):
        """
        Create a new Sapio REST API Client object using API Token. Typically ends with "/webservice/api".

        :param url: The URL of root of REST API APPLICATION. For example: https://localhost/webservice/api
        :param api_token: The API token to authenticate the platform API user. Use App Config Manager to obtain this.
        :param guid: When using username/password authentication, provide GUID of the app. Obtain from Sapio Portal.
        :param username: When using username/password authentication, the username of the credential.
        :param password: When using username/password authentication, the password of the credential.
        :param verify_ssl_cert: Whether to verify SSL certificates. This will throw SSLError if the server self-signed.
        :param timeout_seconds: The wait timeout of the request, in seconds. Default: 60 (1 minute)
        """
        self.url = url
        self.api_token = api_token
        self.guid = guid
        self.username = username
        self.password = password
        self.verify_ssl_cert = verify_ssl_cert
        self.timeout_seconds = timeout_seconds
        self.account_name = account_name
        self.__next_temp_record_id = -1
        self.logger = logging.getLogger("SapioUser")
        self._session_additional_data = session_additional_data
        ensure_logger_initialized(self.logger)
        # CR-51508 Added mandatory alert.
        if not verify_ssl_cert:
            print("[ERROR]: Sapio connection is not secure as SSL is turned off. "
                  "This should not be used in production or any non local environment")
            logging.error("Sapio connection is not secure as SSL is turned off. "
                          "This should not be used in production or any non local environment")

    def get_http_headers(self) -> dict:
        ret = {
            'user-agent': 'SapioAnalyticsPyLib'
        }
        if self.account_name is not None:
            ret["X-ACCOUNT-KEY"] = self.account_name
        if self.username is not None and self.password is not None:
            userpass = self.username + ':' + self.password
            encoded = b64encode(userpass.encode()).decode()
            ret['Authorization'] = "Basic %s" % encoded
        if self.guid is not None:
            ret['X-APP-KEY'] = self.guid
        if self.api_token is not None:
            ret['X-API-TOKEN'] = self.api_token
        return ret

    @staticmethod
    def is_null_response(response: Response):
        text_response = response.text
        if text_response and text_response.strip():
            return False
        return True

    def post(self, url_sub_path: str, params: Optional[dict] = None, payload=None) -> Response:
        return requests.post(self.url + url_sub_path, params=params, json=payload,
                             headers=self.get_http_headers(), verify=self.verify_ssl_cert,
                             timeout=self.timeout_seconds)

    def post_data_stream(self, url_sub_path: str, data_stream: IO, params: Optional[dict] = None):
        headers = self.get_http_headers()
        headers['Content-Type'] = 'application/octet-stream'
        return requests.post(self.url + url_sub_path, params=params, data=data_stream,
                             headers=headers, verify=self.verify_ssl_cert,
                             timeout=self.timeout_seconds)

    def get(self, url_sub_path: str, params: Optional[dict] = None) -> Response:
        return requests.get(self.url + url_sub_path, params=params,
                            headers=self.get_http_headers(), verify=self.verify_ssl_cert,
                            timeout=self.timeout_seconds)

    def consume_octet_stream_get(self, url_sub_path: str,
                                 data_sink: Callable[[bytes], None],
                                 params: Optional[dict] = None,
                                 chunk_size=1024 * 1024) -> None:
        session = requests.Session()
        url = self.url + url_sub_path
        headers = self.get_http_headers()
        response = session.get(url=url, params=params,
                               headers=headers, verify=self.verify_ssl_cert,
                               timeout=self.timeout_seconds, stream=True)
        self.raise_for_status(response)
        for chunk in response.iter_content(chunk_size=chunk_size):
            data_sink(chunk)

    def consume_octet_stream_post(self, url_sub_path: str,
                                  data_sink: Callable[[bytes], None],
                                  params: Optional[dict] = None,
                                  payload = None,
                                  chunk_size=1024 * 1024) -> None:
        session = requests.Session()
        url = self.url + url_sub_path
        headers = self.get_http_headers()
        response = session.post(url=url, params=params, json=payload,
                                headers=headers, verify=self.verify_ssl_cert,
                                timeout=self.timeout_seconds, stream=True)
        self.raise_for_status(response)
        for chunk in response.iter_content(chunk_size=chunk_size):
            data_sink(chunk)

    def delete(self, url_sub_path: str, params: Optional[dict] = None, payload=None) -> Response:
        return requests.delete(self.url + url_sub_path, params=params, json=payload,
                               headers=self.get_http_headers(), verify=self.verify_ssl_cert,
                               timeout=self.timeout_seconds)

    def put(self, url_sub_path: str, params: Optional[dict] = None, payload=None) -> Response:
        return requests.put(self.url + url_sub_path, params=params, json=payload,
                            headers=self.get_http_headers(), verify=self.verify_ssl_cert,
                            timeout=self.timeout_seconds)

    def get_next_temp_record_id(self) -> int:
        cur_id = self.__next_temp_record_id
        self.__next_temp_record_id -= 1
        return cur_id

    @staticmethod
    def raise_for_status(response: Response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise SapioServerException(e)

    @staticmethod
    def build_url(url_list: List[str]) -> str:
        url = '/'.join(urllib.parse.quote(x) for x in url_list)
        if not url.startswith('/'):
            url = '/' + url
        return url

    def log_info(self, msg: str) -> None:
        """
        Log a info message.
        """
        prefix = self.get_logging_prefix()
        self.logger.info(prefix + msg)

    def log_warn(self, msg: str) -> None:
        """
        Log a warning message.
        """
        prefix = self.get_logging_prefix()
        self.logger.info(prefix + msg)

    def log_error(self, msg: str, exc_info=True) -> None:
        """
        Log an error message
        :param msg: The message to log error for
        :param exc_info: If true, it will also print the stack trace.
        """
        prefix = self.get_logging_prefix()
        self.logger.error(prefix + msg, exc_info=exc_info)

    def get_logging_prefix(self):
        """
        Prefix each log from this context with the username and URL of the service.
        """
        prefix: str = "<" + self.url + "> "
        if self.username:
            prefix = self.username + ": "
        return prefix

    @property
    def session_additional_data(self) -> UserSessionAdditionalData:
        if self._session_additional_data is not None:
            return self._session_additional_data
        sub_url = '/user/currentsession/additionaldata'
        response = self.get(sub_url)
        self.raise_for_status(response)
        self._session_additional_data = parse_session_additional_data(response.json())
        return self._session_additional_data
