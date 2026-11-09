from pages.cart_page import CartPage

BACKPACK = "sauce-labs-backpack"
BIKE_LIGHT = "sauce-labs-bike-light"


def test_add_product_to_cart(inventory_page):
    inventory_page.add_to_cart(BACKPACK)

    assert inventory_page.has_remove_button(BACKPACK)
    assert inventory_page.cart_count() == 1


def test_remove_product_from_catalog(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.remove_from_cart(BACKPACK)

    assert not inventory_page.has_remove_button(BACKPACK)
    assert inventory_page.cart_count() == 0


def test_cart_contains_added_products(driver, inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    inventory_page.open_cart()

    assert sorted(CartPage(driver).item_names()) == [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
    ]
