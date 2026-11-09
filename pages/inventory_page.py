from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class InventoryPage:

    TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
    CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def title(self):
        return self.wait.until(EC.visibility_of_element_located(self.TITLE)).text

    def _click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def add_to_cart(self, product):
        """product — часть data-test, например 'sauce-labs-backpack'."""
        self._click((By.CSS_SELECTOR, f'[data-test="add-to-cart-{product}"]'))

    def remove_from_cart(self, product):
        self._click((By.CSS_SELECTOR, f'[data-test="remove-{product}"]'))

    def has_remove_button(self, product):
        return bool(self.driver.find_elements(By.CSS_SELECTOR, f'[data-test="remove-{product}"]'))

    def cart_count(self):
        """Число на значке корзины. Если значка нет — корзина пуста, возвращаем 0."""
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def open_cart(self):
        self._click(self.CART_LINK)
