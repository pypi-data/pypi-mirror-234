import json
import urllib3
import requests
from requests.exceptions import ConnectionError

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class URL:
    LOGIN = "/login"
    REFRESH = "/refresh"


class Response:
    """
    REST API Reponse

    Attributes:
        ok: REST request is ok, status code is 200 or 201
        data: normalized response data
        status_code: REST API request response status code

    """

    def __init__(self):
        self.ok = True
        self.data = None
        self.status_code = -1

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if (
            self.ok != other.ok
            or self.data != other.data
            or self.status_code != other.status_code
        ):
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


class Client:
    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        login_domain: str = "local",
        verify: bool = False,
    ):
        """

        Args:
            url (str): ND mgmt url, https://nd.example.com, https://192.168.1.2
            username (str): Username
            password (str): Password
            login_domain (str): login domain, default is local
            verify (bool): verify SSL ceritificate, default is False

        """
        self._base_url = url
        self._username = username
        self._password = password
        self._login_domain = login_domain
        self._verify = verify
        self._session = requests.session()
        self._headers = {"Content-Type": "application/json"}

    @property
    def url(self):
        return self._base_url

    @property
    def session(self):
        return self._session

    def normalize_resp_data(self, resp: requests.Response) -> dict:
        """

        Args:
            resp (requests.Response):

        Returns:
            dict, if response is json format, return json.loads(data), if response is plaintext, return {"data": requests.Response.text}

        """
        try:
            return resp.json()
        except json.decoder.JSONDecodeError:
            return {"text": resp.text}

    def login(self) -> bool:
        """
        login function should be called once client instance is initialized, client.login()
        Returns:
            bool: True if login success, False if login failed

        """
        data = {
            "userName": self._username,
            "userPasswd": self._password,
            "domain": self._login_domain,
        }
        resp = self.send(endpoint=URL.LOGIN, method="POST", data=data)
        return resp.ok

    def refresh(self) -> bool:
        """
        Refresh Token, this function will be called automatically when Any API is called

        Returns:
            bool: True if refresh success, False if faileed
        """
        resp = self.send(endpoint=URL.REFRESH, method="post")
        return resp.ok

    def _send(self, prep_req: requests.PreparedRequest) -> requests.Response:
        return self.session.send(request=prep_req, verify=self._verify)

    def send(
        self, endpoint: str, method: str, data: dict = None, headers: dict = {}
    ) -> Response:
        """

        Args:
            endpoint (str): API endpoint like "/version"
            method (str): Choose from "get", "post", "put", "delete"
            data (dict): payload in dict, default is None
            headers (dict): addtional headers need to be sent with API, default is {}

        Returns:
            client.Resposne: REST API response

        Raises:
            ValueError: if any input is invalid

        """
        if method.lower() not in ["get", "put", "post", "delete"]:
            raise ValueError(f"Invalid method: {method}")
        if str(endpoint) == "" or not str(endpoint).startswith("/"):
            raise ValueError(f"Invalid API endpoint: {endpoint}")

        rest_url = self._base_url + endpoint
        rest_resp = Response()
        rest_headers = self._headers
        extra_headers = headers
        if headers == {}:
            extra_headers = {}  # normalize the headers

        rest_headers.update(extra_headers)

        req = requests.Request(
            method=method.upper(),
            url=rest_url,
            headers=rest_headers,
            data=json.dumps(data),
        )
        prep_req = self.session.prepare_request(req)
        try:
            if endpoint not in [URL.LOGIN, URL.REFRESH]:
                refreshed = self.refresh()
                if not refreshed:
                    self.login()
            resp = self._send(prep_req=prep_req)
        except ConnectionError as e:
            raise e

        rest_resp.data = self.normalize_resp_data(resp)
        rest_resp.status_code = resp.status_code
        if resp.status_code not in [200, 201]:
            rest_resp.ok = False
        else:
            rest_resp.ok = True
        return rest_resp

    def send_file(self, endpoint: str, data: dict) -> Response:
        """
        special function to upload file

        Args:
            endpoint: upload URL
            data: dictionary with requested parameter, ex:
                  url = "/appcenter/cisco/ndfc/api/v1/imagemanagement/imageupload/smart-image-upload"
                  data = {
                    file: open("nxos64-cs.10.2.4.M.bin", "rb")
                  }
                  send_file(url, data)
        """
        url = self._base_url + endpoint
        rest_resp = Response()
        req = requests.Request(method="POST", url=url, files=data)
        prep_req = self.session.prepare_request(req)
        try:
            if endpoint not in [URL.LOGIN, URL.REFRESH]:
                refreshed = self.refresh()
                if not refreshed:
                    self.login()
            resp = self._send(prep_req=prep_req)
        except ConnectionError as e:
            raise e

        rest_resp.data = self.normalize_resp_data(resp)
        rest_resp.status_code = resp.status_code
        if resp.status_code not in [200, 201]:
            rest_resp.ok = False
        else:
            rest_resp.ok = True
        return rest_resp
