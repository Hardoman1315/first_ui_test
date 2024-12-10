import allure

from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from Pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        self.page_url = 'https://www.saucedemo.com/inventory.html'
        # Кнопка Add to Cart для Sauce Labs Bolt T-Shirt: Здесь будет локатор XPATH
        self.add_tshirt_to_cart_btn = (By.XPATH, '//*[@id="add-to-cart-sauce-labs-bolt-t-shirt"]')
        # Проверка на наличие числа '1' возле корзины
        self.cart_badge = (By.XPATH, '//*[@class="shopping_cart_badge"]')
        # Кнопка корзины: Здесь будет локатор XPATH
        self.cart_btn = (By.XPATH, '//*[@class="shopping_cart_link"]')

    def choose_item(self) -> None:
        self.find_element(*self.item).click()

    @allure.step('Нажать "Add to cart" на предмете "Sauce Labs Bolt T-Shirt"')
    def add_tshirt_to_cart_btn_click(self) -> None:
        self.find_element(*self.add_tshirt_to_cart_btn).click()

    @allure.step('Проверить что число рядом с корзиной равно "1"')
    def cart_badge_number(self) -> None:
        badge_value = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(self.cart_badge)
        )
        assert badge_value.text == '1', (
            '[FAILED] Cart number not equal to "1"'
        )

    @allure.step('Нажать на иконку корзины')
    def cart_btn_click(self) -> str:
        price_text = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '(//*[@class="inventory_item_price"])[3]'))
        ).text
        price_text = price_text.replace('$', '').strip()
        self.find_element(*self.cart_btn).click()
        return price_text

    @allure.step(r'Проверить, что открыта страница "https://www.saucedemo.com/inventory.html"')
    def check_inventory_page_open(self) -> None:
        assert self.get_current_url() == self.page_url, (
         '[FAILED] Login attempt was failed, check login and password'
        )

    @allure.step(r'Проверить, что страница "https://www.saucedemo.com/inventory.html" не открывается')
    def check_inventory_page_not_open(self) -> None:
        assert self.get_current_url() != self.page_url, (
            '[FAILED] Login attempt was not failed with incorrect login and password'
        )
