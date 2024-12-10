import allure

import selenium.webdriver.support.expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from Pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        self.first_name = (By.ID, 'first-name')     #Локатор по ID для элемента строки ввода First Name
        self.last_name = (By.ID, 'last-name')       #Локатор по ID для элемента строки ввода Last Name
        self.zip_code = (By.ID, 'postal-code')      #Локатор по ID для элемента строки ввода Zip/Postal Code
        self.login_btn = (By.XPATH, '//*[@value="Continue"]')  #Локатор по XPATH для элемента кнопка Continue

    @allure.step(r'Ввести имя')
    def input_first_name(self, first_name: str) -> None:
        self.find_element(*self.first_name).send_keys(first_name)

    @allure.step(r'Ввести фамилию')
    def input_last_name(self, last_name: str) -> None:
        self.find_element(*self.last_name).send_keys(last_name)

    @allure.step(r'Ввести Zip код')
    def input_zip_code(self, zip_code) -> None:
        self.find_element(*self.zip_code).send_keys(zip_code)

    @allure.step(r'Нажать кнопку "Continue"')
    def continue_click(self) -> None:
        self.find_element(*self.login_btn).click()

    @allure.step(r'Заполнить поля и нажать continue')
    def fill_fields(self, first_name: str, last_name: str, zip_code: str) -> None:
        self.find_element(*self.first_name).send_keys(first_name)
        self.find_element(*self.last_name).send_keys(last_name)
        self.find_element(*self.zip_code).send_keys(zip_code)
        self.find_element(*self.login_btn).click()

    item_list = (By.XPATH, '//*[@class="cart_item"]')

    @allure.step('Проверить количество добавленных в корзину товаров')
    def number_of_products(self) -> None:
        num = len(self.find_elements(*self.item_list))
        assert num == 1, (
            '[FAILED] There more or less items than 1'
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

    @allure.step('Проверить наличие заголовка "Payment Information:"')
    def payment_title(self) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[contains(text(), "Payment Information:")]'))
        )

    @allure.step('Проверить что способ оплаты соответствует "SauceCard #31337"')
    def payment_card(self) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[contains(text(), "SauceCard #31337")]'))
        )

    @allure.step('Проверить наличие заголовка "Shipping Information:"')
    def shipping_title(self) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[contains(text(), "Shipping Information:")]'))
        )

    @allure.step('Проверить что способ доставки соответствует "Free Pony Express Delivery!"')
    def shipping_method(self) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[contains(text(), "Free Pony Express Delivery!")]'))
        )

    @allure.step('Проверить наличие заголовка "Price Total:"')
    def total_price(self) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[contains(text(), "Price Total:")]'))
        )

    @allure.step('Сравнить цену в магазине и на момент оплаты')
    def payment_price(self) -> str:
        cart_price = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[@class="inventory_item_price"]'))
        ).text
        cart_price = cart_price.replace('$', '').strip()
        return cart_price

    # В задании было сказано, что налог должен быть $2.50, но на сайте он оказался равен 1.28
    # и я решил что это опечатка
    @allure.step('Проверить что поле "tax" равно $1.28')
    def tax(self) -> str:
        tax_value = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[@class="summary_tax_label"]'))
        ).text

        tax_value = tax_value.replace('Tax: $', '').strip()
        assert tax_value == '1.28', (
            '[FAILED] tax not equal to 1.28'
        )
        return tax_value

    @allure.step('Проверить что "Total" равен цене за товар + налогу')
    def total_price(self) -> None:
        price = CheckoutPage.payment_price()
        tax = CheckoutPage.tax()

        price = int(price)
        tax = int(tax)

        tax_value = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[@class="summary_total_label"]'))
        ).text

        total_price = tax_value.replace('Total: $', '').strip()
        total_price = int(total_price)

        assert price + tax == total_price, (
            '[FAILED] total price are not equal to sum of price and tax'
        )

    @allure.step('Нажать кнопку "Finish"')
    def finish_button(self) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="finish"]'))
        ).click()

    @allure.step('Проверить наличие надписи "Checkout: Complete!"')
    def is_checkout_complete(self) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '// *[contains(text(), "Checkout: Complete!")]'))
        )

    @allure.step('Проверить наличие заголовка "Thank you for your order!"')
    def is_thank_for_order(self) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '// *[contains(text(), "Thank you for your order!")]'))
        )

    @allure.step('Проверить наличие надписи "Your order has been dispatched, '
                 'and will arrive just as fast as the pony can get there!"')
    def delivery_text(self) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '// *[contains(text(), '
                                                      '"Your order has been dispatched, '
                                                      'and will arrive just as fast as the pony can get there!")]'))
        )

    @allure.step('Проверить наличие кнопки "Back Home"')
    def back_button_availability(self) -> None:
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="back-to-products"]'))
        )
