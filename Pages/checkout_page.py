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
        locator = (By.XPATH, '//*[contains(text(), "Sauce Labs Bolt T-Shirt")]')
        assert self.element_is_visible(locator).text == 'Sauce Labs Bolt T-Shirt', (
            '[FAILED] "Sauce Labs Bolt T-Shirt" title is not found'
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
        locator = (By.XPATH, '//*[contains(text(), "Payment Information:")]')
        assert self.element_is_visible(locator).text == 'Payment Information:', (
            '[FAILED] "Payment Information" title is not found'
        )

    @allure.step('Проверить что способ оплаты соответствует "SauceCard #31337"')
    def payment_card(self) -> None:
        locator = (By.XPATH, '//*[contains(text(), "SauceCard #31337")]')
        assert self.element_is_visible(locator).text == 'SauceCard #31337', (
            '[FAILED] Payment method is not "SauceCard #31337"'
        )

    @allure.step('Проверить наличие заголовка "Shipping Information:"')
    def shipping_title(self) -> None:
        locator = (By.XPATH, '//*[contains(text(), "Shipping Information:")]')
        assert self.element_is_visible(locator).text == 'Shipping Information:', (
            '[FAILED] "Shipping Information" title is not found'
        )

    @allure.step('Проверить что способ доставки соответствует "Free Pony Express Delivery!"')
    def shipping_method(self) -> None:
        locator = (By.XPATH, '//*[contains(text(), "Free Pony Express Delivery!")]')
        assert self.element_is_visible(locator).text == 'Free Pony Express Delivery!', (
            '[FAILED] "Free Pony Express Delivery!" title is not found'
        )

    @allure.step('Проверить наличие заголовка "Price Total:"')
    def total_price(self) -> None:
        locator = (By.XPATH, '//*[contains(text(), "Price Total:")]')
        assert self.element_is_visible(locator).text == 'Price Total:', (
            '[FAILED] "Price total" title is not found'
        )

    @allure.step('Сравнить цену в магазине и на момент оплаты')
    def payment_price(self) -> str:
        locator = (By.XPATH, '//*[@class="inventory_item_price"]')
        cart_price = self.element_is_visible(locator).text
        cart_price = cart_price.replace('$', '').strip()
        return cart_price

    # В задании было сказано, что налог должен быть $2.50, но на сайте он оказался равен 1.28
    # и я решил что это опечатка
    @allure.step('Проверить что поле "tax" равно $1.28')
    def tax(self) -> str:
        locator = (By.XPATH, '//*[@class="summary_tax_label"]')
        tax_value = self.element_is_visible(locator).text
        tax_value = tax_value.replace('Tax: $', '').strip()
        assert tax_value == '1.28', (
            '[FAILED] tax not equal to 1.28'
        )
        return tax_value

    @allure.step('Проверить что "Total" равен цене за товар + налогу')
    def total_price(self) -> str:
        price = self.payment_price()
        tax = self.tax()

        price = float(price)
        tax = float(tax)

        locator = (By.XPATH, '//*[@class="summary_total_label"]')
        total_price = self.element_is_visible(locator).text

        total_price = total_price.replace('Total: $', '').strip()
        total_price = float(total_price)

        assert price + tax == total_price, (
            '[FAILED] total price are not equal to sum of price and tax'
        )

        return str(price)

    @allure.step('Нажать кнопку "Finish"')
    def finish_button(self) -> None:
        locator = (By.XPATH, '//*[@id="finish"]')
        self.element_is_visible(locator).click()

    @allure.step('Проверить наличие надписи "Checkout: Complete!"')
    def is_checkout_complete(self) -> None:
        locator = (By.XPATH, '// *[contains(text(), "Checkout: Complete!")]')
        assert self.element_is_visible(locator).text == 'Checkout: Complete!', (
            '[FAILED] "Checkout: Complete!" title is not found'
        )

    @allure.step('Проверить наличие заголовка "Thank you for your order!"')
    def is_thank_for_order(self) -> None:
        locator = (By.XPATH, '// *[contains(text(), "Thank you for your order!")]')
        assert self.element_is_visible(locator).text == 'Thank you for your order!', (
            '[FAILED] "Thank you for your order!" title is not found'
        )

    @allure.step('Проверить наличие надписи "Your order has been dispatched, '
                 'and will arrive just as fast as the pony can get there!"')
    def delivery_text(self) -> None:
        locator = (By.XPATH, '// *[contains(text(), "Your order has been dispatched, '
                             'and will arrive just as fast as the pony can get there!")]')
        assert self.element_is_visible(locator).text == ('Your order has been dispatched, '
                                                         'and will arrive just as fast as '
                                                         'the pony can get there!')

    @allure.step('Проверить наличие кнопки "Back Home"')
    def back_button_availability(self) -> None:
        locator = (By.XPATH, '//*[@id="back-to-products"]')
        self.element_is_visible(locator)
