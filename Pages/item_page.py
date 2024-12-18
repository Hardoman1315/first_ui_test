from selenium.webdriver.common.by import By
from Pages.base_page import BasePage


class ItemPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        # Кнопка Add to Cart: Здесь будет локатор XPATH
        self.add_to_cart_btn = (By.XPATH, '//*[@name="add-to-cart"]')
        # Кнопка Back to products: Здесь будет локатор XPATH
        self.back_to_products = (By.XPATH, '//*[@name="back-to-products"]')

    def add_to_cart_btn_click(self):
        self.click_element(self.add_to_cart_btn)

    def return_to_products(self):
        self.click_element(self.back_to_products)
