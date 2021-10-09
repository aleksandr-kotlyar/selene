import os

import pytest

from selene import Config, Browser
from tests.helpers import chrome_driver


def pytest_addoption(parser):
    parser.addoption(
        '--headless',
        help='headless mode',
        default='0',
        choices=['0', '1'],
    )


@pytest.fixture(scope='session', autouse=True)
def headless(request):
    os.environ['HEADLESS'] = request.config.getoption('--headless')


@pytest.fixture(scope='session', autouse=True)
def wdm_logs():
    os.environ['WDM_LOG_LEVEL'] = '0'


@pytest.fixture(scope='session')
def session_chrome_driver():
    driver = chrome_driver()
    yield driver
    driver.quit()


@pytest.fixture(scope='function')
def session_browser(session_chrome_driver):
    yield Browser(Config(driver=session_chrome_driver))


@pytest.fixture(scope='function')
def function_browser():
    driver = chrome_driver()
    yield Browser(Config(driver=driver))
    driver.quit()
