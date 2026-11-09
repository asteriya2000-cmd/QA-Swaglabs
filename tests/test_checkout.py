import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

BACKPACK = "sauce-labs-backpack"
BIKE_LIGHT = "sauce-labs-bike-light"
TAX_RATE = 0.08


def go_to_overview(driver, inventory_page):
    inventory_page.open_cart()
    CartPage(driver).start_checkout()
    checkout = CheckoutPage(driver)
    checkout.fill_form("Anna", "Ivanova", "190000")
    checkout.continue_to_overview()
    return checkout


def test_checkout_happy_path(driver, inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    checkout = go_to_overview(driver, inventory_page)
    checkout.finish()

    assert checkout.complete_message() == "Thank you for your order!"


def test_order_total_is_calculated_correctly(driver, inventory_page):
    inventory_page.add_to_cart(BACKPACK)      # $29.99
    inventory_page.add_to_cart(BIKE_LIGHT)    # $9.99
    checkout = go_to_overview(driver, inventory_page)

    subtotal = checkout.subtotal()
    assert subtotal == pytest.approx(39.98)
    assert checkout.tax() == pytest.approx(round(subtotal * TAX_RATE, 2))
    assert checkout.total() == pytest.approx(subtotal + checkout.tax())


@pytest.mark.xfail(
    reason="BUG-001: сайт позволяет оформить заказ с пустой корзиной",
    strict=True,
)
def test_checkout_is_blocked_for_empty_cart(driver, inventory_page):
    inventory_page.open_cart()
    CartPage(driver).start_checkout()

    try:
        WebDriverWait(driver, 3).until(EC.url_contains("checkout-step-one"))
        checkout_opened = True
    except TimeoutException:
        checkout_opened = False

    assert not checkout_opened, "Оформление заказа открылось при пустой корзине"
