import pytest
import requests
from urllib.parse import urljoin
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests import Response
from dotenv import load_dotenv
import os
pytest_plugins = ["docker_compose"]

# @pytest.fixture(scope='session', autouse=True)
# def load_env(request):
#     # load_dotenv(dotenv_path='test.env')
#     os.environ['PORT'] = '9000'

# Invoking this fixture: 'function_scoped_container_getter' starts all services
@pytest.fixture(scope="session")
def wait_for_api(session_scoped_container_getter):
    """Wait for the api from my_api_service to become responsive"""
    request_session = requests.Session()
    retries = Retry(total=10,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    request_session.mount('http://', HTTPAdapter(max_retries=retries))

    service = session_scoped_container_getter.get("web").network_info[0]
    api_url = "http://%s:%s/" % (service.hostname, service.host_port)
    assert request_session.get(api_url)
    yield request_session, api_url


def test_read_and_write(wait_for_api):
    """The Api is now verified good to go and tests can interact with it"""
    request_session, api_url = wait_for_api
    resp: Response = request_session.get(api_url)
    assert resp.status_code == 200
    resp: Response = request_session.get(api_url + 'gradio/')
    assert resp.status_code == 200

