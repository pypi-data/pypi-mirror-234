import pytest

from kognic.io.client import KognicIOClient

ORGANIZATION_ID = 1


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--env", action="store", default="development", help="env can be staging or development")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def organization_id():
    return ORGANIZATION_ID


@pytest.fixture(autouse=True, scope="session")
def client(env: str, organization_id: int) -> KognicIOClient:
    """
    Factory to use the IO Client
    """

    if env == "development" or env is None:
        auth_host = "http://kognic.test:8001"
        host = "http://kognic.test:8010"
    elif env == "staging":
        auth_host = "https://user.staging.kognic.com"
        host = "https://input.staging.kognic.com"
    else:
        raise RuntimeError(f"ENV: {env} is not supported")
    return KognicIOClient(auth=None, auth_host=auth_host, host=host, client_organization_id=organization_id)
