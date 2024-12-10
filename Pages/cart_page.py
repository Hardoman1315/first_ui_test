import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec

from Pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        # Локатор XPATH элемента продукта. Локатор должен
        # находить ровно 1 элемент на странице:
        self.item_list = (By.XPATH, '//*[@class="cart_item"]')
        # Кнопка "checkout"
        self.checkout_button = (By.XPATH, '//*[@id="checkout"]')

    @allure.step('Проверить количество добавленных в корзину товаров')
    def number_of_products(self) -> None:
        num = len(self.find_elements(*self.item_list))
        assert num == 1, (
        '[FAILED] Cart have more or less items than 1'
    )

    @allure.step('Проверить наличие "Sauce Labs Bolt T-Shirt"')
    def tshirt_availability(self) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[contains(text(), "Sauce Labs Bolt T-Shirt")]'))
        )

    @allure.step('Сравнить цену в магазине и корзине')
    def compare_price(self) -> str:
        cart_price = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[@class="inventory_item_price"]'))
        ).text
        cart_price = cart_price.replace('$', '').strip()
        return cart_price

    @allure.step('Нажать кнопку "checkout"')
    def checkout_click(self) -> None:
        self.find_element(*self.checkout_button).click()
