import allure
from selenium.webdriver.common.by import By
from Pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

    # Локатор XPATH элемента продукта. Локатор должен
    # находить ровно 1 элемент на странице:
    item_list = (By.XPATH, '//*[@class="cart_item"]')
    # Кнопка "checkout"
    checkout_button = (By.XPATH, '//*[@id="checkout"]')
    tshirt_title = (By.XPATH, '//*[@class="inventory_item_name"]')
    cart_price = (By.XPATH, '//*[@class="inventory_item_price"]')


    @allure.step('Сравнить количество добавленных в корзину товаров')
    def compare_number_of_products(self) -> None:
        assert len(self.elements_is_visible(self.item_list)) == 1, (
        '[FAILED] Cart have more or less items than 1'
    )

    @allure.step('Проверить наличие "Sauce Labs Bolt T-Shirt"')
    def check_tshirt_availability(self) -> None:
        assert self.get_element_text(self.tshirt_title) == 'Sauce Labs Bolt T-Shirt', (
            '[FAILED] "Sauce Labs Bolt T-Shirt" title not found'
        )

    @allure.step('Сравнить цену в магазине и корзине')
    def get_price(self) -> str:
        price_value = self.get_element_text(self.cart_price)
        price_value = price_value.replace('$', '').strip()
        return price_value

    @allure.step('Нажать кнопку "checkout"')
    def click_checkout(self) -> None:
        self.click_element(self.checkout_button)
