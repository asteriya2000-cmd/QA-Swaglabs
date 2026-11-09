from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CheckoutPage:

    FIRST_NAME = (By.CSS_SELECTOR, '[data-test="firstName"]')
    LAST_NAME = (By.CSS_SELECTOR, '[data-test="lastName"]')
    POSTAL_CODE = (By.CSS_SELECTOR, '[data-test="postalCode"]')
    CONTINUE_BUTTON = (By.CSS_SELECTOR, '[data-test="continue"]')
    FINISH_BUTTON = (By.CSS_SELECTOR, '[data-test="finish"]')
    SUBTOTAL = (By.CSS_SELECTOR, '[data-test="subtotal-label"]')
    TAX = (By.CSS_SELECTOR, '[data-test="tax-label"]')
    TOTAL = (By.CSS_SELECTOR, '[data-test="total-label"]')
    COMPLETE_HEADER = (By.CSS_SELECTOR, '[data-test="complete-header"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def _visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def fill_form(self, first_name, last_name, postal_code):
        self._visible(self.FIRST_NAME).send_keys(first_name)
        self._visible(self.LAST_NAME).send_keys(last_name)
        self._visible(self.POSTAL_CODE).send_keys(postal_code)

    def continue_to_overview(self):
        self._click(self.CONTINUE_BUTTON)

    def finish(self):
        self._click(self.FINISH_BUTTON)

    def _amount(self, locator):
        text = self._visible(locator).text
        return float(text.split("$")[1])

    def subtotal(self):
        return self._amount(self.SUBTOTAL)

    def tax(self):
        return self._amount(self.TAX)

    def total(self):
        return self._amount(self.TOTAL)

    def complete_message(self):
        return self._visible(self.COMPLETE_HEADER).text
