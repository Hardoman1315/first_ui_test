import allure
from selenium.webdriver.common.by import By
from Pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        self.page_url = 'https://www.saucedemo.com/inventory.html'

    @allure.step('Нажать "Add to cart" на предмете "Sauce Labs Bolt T-Shirt"')
    def add_tshirt_to_cart_btn_click(self) -> None:
        locator = (By.XPATH, '//*[@id="add-to-cart-sauce-labs-bolt-t-shirt"]')
        self.element_is_visible(locator).click()

    @allure.step('Проверить что число рядом с корзиной равно "1"')
    def cart_badge_number(self) -> None:
        locator = (By.XPATH, '//*[@class="shopping_cart_badge"]')
        badge_value = self.element_is_visible(locator)
        assert badge_value.text == '1', (
            '[FAILED] Cart number not equal to "1"'
        )

    @allure.step('Получить цену товара в магазине')
    def get_price(self):
        locator = (By.XPATH, '(//*[@class="inventory_item_price"])[3]')
        price_text = self.element_is_visible(locator).text
        price_text = price_text.replace('$', '').strip()
        return price_text

    @allure.step('Нажать на иконку корзины')
    def cart_btn_click(self) -> str:
        locator = (By.XPATH, '//*[@class="shopping_cart_link"]')
        self.element_is_visible(locator).click()
