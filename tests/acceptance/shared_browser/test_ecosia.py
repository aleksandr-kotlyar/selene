# MIT License
#
# Copyright (c) 2015-2022 Iakiv Kramarenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import pytest

from selene import by, have
from selene.support.shared import browser


@pytest.fixture(scope='function')
def close():
    yield
    browser.quit()


@pytest.mark.parametrize(
    'browser_name, expected_browser_name',
    [
        ('firefox', 'firefox'),
        ('edge', 'msedge'),
        ('opera', 'opera'),
        ('chrome', 'chrome'),
        ('ie', 'ie'),
    ]
)
def test_search(browser_name, expected_browser_name, close):
    browser.config.browser_name = browser_name

    browser.open('https://www.ecosia.org/')
    browser.element(by.name('q')).type(
        'github yashaka selene python'
    ).press_enter()

    browser.all('.web-result').first.element('.result__link').click()
    browser.should(have.title_containing('yashaka/selene'))
    assert browser.driver.name == expected_browser_name
