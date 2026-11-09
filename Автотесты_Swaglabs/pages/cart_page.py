from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CartPage:

    ITEM_NAMES = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, '[data-test="checkout"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def _wait_loaded(self):
        """Ждём, пока откроется именно страница корзины, а не предыдущая."""
        self.wait.until(EC.url_contains("cart.html"))
        self.wait.until(EC.visibility_of_element_located(self.CHECKOUT_BUTTON))

    def item_names(self):
        self._wait_loaded()
        return [item.text for item in self.driver.find_elements(*self.ITEM_NAMES)]

    def start_checkout(self):
        self._wait_loaded()
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON)).click()
