import os
import time
from datetime import datetime

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
def session_browser(session_chrome_driver, request):
    yield Browser(Config(driver=session_chrome_driver))

    if request.node.rep_setup.failed:
        print("setting up a test failed!", request.node.nodeid)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            driver = request.node.funcargs['session_browser'].driver
            take_screenshot(driver, request.node.nodeid)
            print("executing test failed", request.node.nodeid)


@pytest.fixture(scope='function')
def function_browser(request):
    driver = chrome_driver()

    yield Browser(Config(driver=driver))

    if request.node.rep_setup.failed:
        print("setting up a test failed!", request.node.nodeid)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            driver = request.node.funcargs['function_browser'].driver
            take_screenshot(driver, request.node.nodeid)
            print("executing test failed", request.node.nodeid)

    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Set up a hook to be able to check if a test has failed."""
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


def take_screenshot(driver, nodeid):
    """Make a screenshot with a name of the test, date and time."""
    time.sleep(1)
    file_name = (
        f'{nodeid}_{datetime.today().strftime("%Y-%m-%d_%H:%M")}.png'
        .replace("/", "_").replace("::", "__")
    )
    driver.save_screenshot(file_name)
