# MIT License
#
# Copyright (c) 2015-2021 Iakiv Kramarenko
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

from selene.core.exceptions import TimeoutException
from selene.support.conditions import be


def test_wait_until_progress_bar_disappears_in_time(function_browser):
    """Test for page with progress bar that appears each time after click on a button.

    Test should use wait_until for progress bar to disappear
        if disappeared:
            pass the test
        else
            fail the test
    """
    show_dialog_btn = function_browser.element('.btn-primary')
    dialog = function_browser.element('.modal-backdrop.fade.in')
    function_browser.open(
        'https://www.seleniumeasy.com/test/bootstrap-progress-bar-dialog-demo.html'
    )

    show_dialog_btn.click()
    dialog.should(be.visible)
    disappeared = dialog.wait_until(be.not_.present)

    assert disappeared is True


def test_wait_until_progress_bar_does_not_disappear_in_time(function_browser):
    """Test for page with progress bar that appears each time after click on a button.

    Test should use wait_until for progress bar to not disappear in timeout
        if not disappeared:
            pass the test
        else
            fail the test
    """
    show_dialog_btn = function_browser.element('.btn-primary')
    dialog = function_browser.element('.modal-backdrop.fade.in')
    function_browser.open(
        'https://www.seleniumeasy.com/test/bootstrap-progress-bar-dialog-demo.html'
    )

    show_dialog_btn.click()
    dialog.should(be.visible)
    disappeared = dialog.with_(timeout=1).wait_until(be.not_.present)

    assert disappeared is False


def test_wait_at_most_progress_bar_disappears_in_time(function_browser):
    """Test for page with progress bar that appears each time after click on a button.

    Test should use wait_until for progress bar to disappear
        if disappeared:
            pass the test
        else
            fail the test
    """
    show_dialog_btn = function_browser.element('.btn-primary')
    dialog = function_browser.element('.modal-backdrop.fade.in')
    function_browser.open(
        'https://www.seleniumeasy.com/test/bootstrap-progress-bar-dialog-demo.html'
    )

    show_dialog_btn.click()
    dialog.should(be.visible)
    dialog.wait.at_most(4).for_(be.not_.present)
    disappeared = dialog.matching(be.not_.present)

    assert disappeared is True


def test_wait_at_most_progress_bar_does_not_disappear_in_time(
    function_browser,
):
    """Test for page with progress bar that appears each time after click on a button.

    Test should use wait_until for progress bar to not disappear in timeout
        if not disappeared:
            pass the test
        else
            fail the test
    """
    show_dialog_btn = function_browser.element('.btn-primary')
    dialog = function_browser.element('.modal-backdrop.fade.in')
    function_browser.open(
        'https://www.seleniumeasy.com/test/bootstrap-progress-bar-dialog-demo.html'
    )

    show_dialog_btn.click()
    dialog.should(be.visible)
    with pytest.raises(TimeoutException) as ex:
        dialog.wait.at_most(1).for_(be.not_.present)

    disappeared = dialog.matching(be.not_.present)
    assert disappeared is False
