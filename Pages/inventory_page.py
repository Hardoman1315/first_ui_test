import allure
from selenium.webdriver.common.by import By
from Pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        self.page_url = 'https://www.saucedemo.com/inventory.html'

    tshirt_btn = (By.XPATH, '//*[@id="add-to-cart-sauce-labs-bolt-t-shirt"]')
    cart_badge = (By.XPATH, '//*[@class="shopping_cart_badge"]')
    item_price = (By.XPATH, '(//*[@class="inventory_item_price"])[3]')
    cart_btn = (By.XPATH, '//*[@class="shopping_cart_link"]')

    @allure.step('Нажать "Add to cart" на предмете "Sauce Labs Bolt T-Shirt"')
    def add_tshirt_to_cart_btn_click(self) -> None:
        self.click_element(self.tshirt_btn)

    @allure.step('Проверить что число рядом с корзиной равно "1"')
    def compare_cart_badge_number(self) -> None:
        assert self.get_element_text(self.cart_badge) == '1', (
            '[FAILED] Cart number not equal to "1"'
        )

    @allure.step('Получить цену товара в магазине')
    def get_price(self):
        price_text = self.get_element_text(self.item_price)
        price_text = price_text.replace('$', '').strip()
        return price_text

    @allure.step('Нажать на иконку корзины')
    def cart_btn_click(self) -> None:
        self.click_element(self.cart_btn)
