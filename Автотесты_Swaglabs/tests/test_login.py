import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_successful_login(driver):
    LoginPage(driver).open().login("standard_user", "secret_sauce")

    assert "/inventory.html" in driver.current_url
    assert InventoryPage(driver).title() == "Products"


@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        pytest.param(
            "locked_out_user", "secret_sauce",
            "Epic sadface: Sorry, this user has been locked out.",
            id="TC-AUTH-02-locked-out-user",
        ),
        pytest.param(
            "standard_user", "wrong_pass",
            "Epic sadface: Username and password do not match any user in this service",
            id="TC-AUTH-03-wrong-password",
        ),
        pytest.param(
            "", "secret_sauce",
            "Epic sadface: Username is required",
            id="TC-AUTH-05-empty-username",
        ),
        pytest.param(
            "standard_user", "",
            "Epic sadface: Password is required",
            id="TC-AUTH-06-empty-password",
        ),
    ],
)
def test_login_with_invalid_data(driver, username, password, expected_error):
    login_page = LoginPage(driver).open()
    login_page.login(username, password)

    assert login_page.error_text() == expected_error
    assert "/inventory.html" not in driver.current_url
