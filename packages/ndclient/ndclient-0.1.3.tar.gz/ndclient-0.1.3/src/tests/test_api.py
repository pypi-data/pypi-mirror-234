import json
import pytest
import requests_mock
from ndclient import Client, Response

url = "https://nd.test.org"
username = "admin"
password = "password"
login_domain = "cisco"
verify = True
resource_folder = "src/tests/resources/"


@pytest.fixture()
def version_info():
    with open(resource_folder + "version.json") as f:
        return f.read()


@pytest.fixture()
def login_response():
    with open(resource_folder + "login.json") as f:
        return f.read()


@pytest.fixture()
def refresh_response():
    with open(resource_folder + "refresh.json") as f:
        return f.read().strip()


@pytest.fixture()
def refresh_response_fail():
    with open(resource_folder + "refresh_fail.json") as f:
        return f.read().strip()


@pytest.fixture()
def image_file():
    return open(resource_folder + "nxos64-cs.10.2.4.M.bin")


@pytest.fixture()
def upload_response():
    with open(resource_folder + "upload.txt") as f:
        return f.read().strip()


@pytest.fixture()
def version_url():
    return "/appcenter/cisco/ndfc/api/v1/fm/about/version"


@pytest.fixture()
def upload_url():
    return "/appcenter/cisco/ndfc/api/v1/imagemanagement/imageupload/smart-image-upload"


def test_property():
    client = Client(url, username, password, login_domain, verify)
    assert client.url == url


def test_Response():
    resp1 = Response()
    resp1.ok = True
    resp1.data = {"text": "1"}
    resp2 = ""
    resp3 = Response()
    resp3.ok = True
    resp3.data = {"text": "2"}
    assert resp1 != resp2
    assert resp1 != resp3
    resp3.data = {"text": "1"}
    assert resp1 == resp3


def test_send_negative():
    client = Client(url, username, password, login_domain, verify)
    try:
        client.send("test", "get")
    except ValueError:
        pass

    try:
        client.send("/test", "mget")
    except ValueError:
        pass


@requests_mock.Mocker(kw="requests_mocker")
def test_get_version(
    version_url, version_info, login_response, refresh_response_fail, **kwargs
):
    kwargs["requests_mocker"].register_uri("GET", url + version_url, text=version_info)
    kwargs["requests_mocker"].register_uri(
        "POST", url + "/refresh", status_code=500, text=refresh_response_fail
    )
    kwargs["requests_mocker"].register_uri("POST", url + "/login", text=login_response)
    client = Client(url, username, password, login_domain, verify)
    login = client.login()
    assert login

    version = client.send(version_url, "get")
    resp = Response()
    resp.ok = True
    resp.data = json.loads(version_info)
    resp.status_code = 200
    print(version.data)
    assert version == resp


@requests_mock.Mocker(kw="requests_mocker")
def test_login(login_response, **kwargs):
    kwargs["requests_mocker"].register_uri("POST", url + "/login", text=login_response)
    client = Client(url, username, password, login_domain, verify)
    login = client.login()
    assert login


@requests_mock.Mocker(kw="requests_mocker")
def test_refresh(refresh_response, refresh_response_fail, **kwargs):
    kwargs["requests_mocker"].register_uri(
        "POST", url + "/refresh", text=refresh_response
    )

    client = Client(url, username, password, login_domain, verify)
    refresh = client.refresh()
    assert refresh

    kwargs["requests_mocker"].register_uri(
        "POST", url + "/refresh", status_code=500, text=refresh_response_fail
    )
    client = Client(url, username, password, login_domain, verify)
    refresh = client.refresh()
    assert not refresh


@requests_mock.Mocker(kw="requests_mocker")
def test_file_upload(
    upload_url,
    image_file,
    upload_response,
    login_response,
    refresh_response_fail,
    **kwargs,
):
    kwargs["requests_mocker"].register_uri(
        "POST", url + upload_url, text=upload_response
    )
    kwargs["requests_mocker"].register_uri("POST", url + "/login", text=login_response)
    kwargs["requests_mocker"].register_uri(
        "POST", url + "/refresh", text=refresh_response_fail, status_code=500
    )

    data = {"file": image_file}

    client = Client(url, username, password, login_domain, verify)
    r = client.send_file(upload_url, data)
    print(r.data)
    resp = Response()
    resp.ok = True
    resp.data = {"text": upload_response}
    resp.status_code = 200
    assert r == resp
