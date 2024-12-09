import pytest
import logistro as logging



def pytest_addoption(parser):
    logging.customize_pytest_addoption(parser)


@pytest.fixture()
def human(request):
    return request.config.getoption("--logistro_human")