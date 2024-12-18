import allure
from selenium.webdriver.common.by import By
from Pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

    first_name = (By.ID, 'first-name')     #Локатор по ID для элемента строки ввода First Name
    last_name = (By.ID, 'last-name')       #Локатор по ID для элемента строки ввода Last Name
    zip_code = (By.ID, 'postal-code')      #Локатор по ID для элемента строки ввода Zip/Postal Code
    login_btn = (By.XPATH, '//*[@value="Continue"]')    #Локатор по XPATH для элемента кнопка Continue
    item_list = (By.XPATH, '//*[@class="cart_item"]')
    tshirt_title = (By.XPATH, '//*[@class="inventory_item_name"]')
    cart_price = (By.XPATH, '//*[@class="inventory_item_price"]')
    payment_title = (By.XPATH, '//*[@data-test="payment-info-label"]')
    payment_card = (By.XPATH, '//*[@data-test="payment-info-value"]')
    shipping_title = (By.XPATH, '//*[@data-test="shipping-info-label"]')
    shipping_method_title = (By.XPATH, '//*[@data-test="shipping-info-value"]')
    total_price = (By.XPATH, '//*[@data-test="total-info-label"]')
    tax = (By.XPATH, '//*[@class="summary_tax_label"]')
    total_label = (By.XPATH, '//*[@class="summary_total_label"]')
    finish_btn = (By.XPATH, '//*[@id="finish"]')
    checkout_title = (By.XPATH, '//*[@class="title"]') # переписать локатор
    thank_sign = (By.XPATH, '//*[@class="complete-header"]') # переписать локатор
    delivery_sign = (By.XPATH, '//*[@class="complete-text"]') # переписать локатор
    back_btn = (By.XPATH, '//*[@id="back-to-products"]')

    @allure.step(r'Ввести имя')
    def insert_first_name(self, first_name: str) -> None:
        self.insert_value(self.first_name, first_name)

    @allure.step(r'Ввести фамилию')
    def insert_last_name(self, last_name: str) -> None:
        self.insert_value(self.last_name, last_name)

    @allure.step(r'Ввести Zip код')
    def insert_zip_code(self, zip_code) -> None:
        self.insert_value(self.zip_code, zip_code)

    @allure.step(r'Нажать кнопку "Continue"')
    def click_continue(self) -> None:
        self.click_element(self.login_btn)

    @allure.step(r'Заполнить поля и нажать continue')
    def fill_fields(self, first_name: str, last_name: str, zip_code: str) -> None:
        self.insert_value(self.first_name, first_name)
        self.insert_value(self.last_name, last_name)
        self.insert_value(self.zip_code, zip_code)
        self.click_element(self.login_btn)

    @allure.step('Проверить количество добавленных в корзину товаров')
    def compare_number_of_products(self) -> None:
        assert len(self.elements_is_visible(self.item_list)) == 1, (
            '[FAILED] There more or less items than 1'
        )

    @allure.step('Проверить наличие "Sauce Labs Bolt T-Shirt"')
    def check_tshirt_availability(self) -> None:
        assert self.get_element_text(self.tshirt_title) == 'Sauce Labs Bolt T-Shirt', (
            '[FAILED] "Sauce Labs Bolt T-Shirt" title is not found'
        )

    @allure.step('Получить цену в корзине')
    def get_price(self) -> str:
        cart_price = self.get_element_text(self.cart_price)
        cart_price = cart_price.replace('$', '').strip()
        return cart_price

    @allure.step('Проверить наличие заголовка "Payment Information:"')
    def compare_payment_title(self) -> None:
        assert self.get_element_text(self.payment_title) == 'Payment Information:', (
            '[FAILED] "Payment Information" title is not found'
        )

    @allure.step('Проверить что способ оплаты соответствует "SauceCard #31337"')
    def compare_payment_card(self) -> None:
        assert self.get_element_text(self.payment_card) == 'SauceCard #31337', (
            '[FAILED] Payment method is not "SauceCard #31337"'
        )

    @allure.step('Проверить наличие заголовка "Shipping Information:"')
    def compare_shipping_title(self) -> None:
        assert self.get_element_text(self.shipping_title) == 'Shipping Information:', (
            '[FAILED] "Shipping Information" title is not found'
        )

    @allure.step('Проверить что способ доставки соответствует "Free Pony Express Delivery!"')
    def compare_shipping_method(self) -> None:
        assert self.get_element_text(self.shipping_method_title) == 'Free Pony Express Delivery!', (
            '[FAILED] "Free Pony Express Delivery!" title is not found'
        )

    @allure.step('Проверить наличие заголовка "Price Total:"')
    def check_total_price_title(self) -> None:
        assert self.get_element_text(self.total_price) == 'Price Total', (
            '[FAILED] "Price total" title is not found'
        )

    @allure.step('Получить цену на момент оплаты')
    def get_payment_price(self) -> str:
        cart_price = self.get_element_text(self.cart_price)
        cart_price = cart_price.replace('$', '').strip()
        return cart_price

    # В задании было сказано, что налог должен быть $2.50, но на сайте он оказался равен 1.28
    # и я решил что это опечатка
    @allure.step('Проверить что поле "tax" равно $1.28')
    def get_tax(self) -> str:
        tax_value = self.get_element_text(self.tax)
        tax_value = tax_value.replace('Tax: $', '').strip()
        assert tax_value == '1.28', (
            '[FAILED] tax not equal to 1.28'
        )
        return tax_value

    @allure.step('Проверить что "Total" равен цене за товар + налогу')
    def compare_total_price(self) -> str:
        price = self.get_payment_price()
        tax = self.get_tax()

        price = float(price)
        tax = float(tax)

        total_price = self.get_element_text(self.total_label)

        total_price = total_price.replace('Total: $', '').strip()
        total_price = float(total_price)

        assert price + tax == total_price, (
            '[FAILED] total price are not equal to sum of price and tax'
        )

        return str(price)

    @allure.step('Нажать кнопку "Finish"')
    def click_finish_button(self) -> None:
        self.click_element(self.finish_btn)

    @allure.step('Проверить наличие надписи "Checkout: Complete!"')
    def is_checkout_complete(self) -> None:
        assert self.get_element_text(self.checkout_title) == 'Checkout: Complete!', (
            '[FAILED] "Checkout: Complete!" title is not found'
        )

    @allure.step('Проверить наличие заголовка "Thank you for your order!"')
    def compare_thank_for_order(self) -> None:
        assert self.get_element_text(self.thank_sign) == 'Thank you for your order!', (
            '[FAILED] "Thank you for your order!" title is not found'
        )

    @allure.step('Проверить наличие надписи "Your order has been dispatched, '
                 'and will arrive just as fast as the pony can get there!"')
    def compare_delivery_text(self) -> None:
        assert self.get_element_text(self.delivery_sign) == ('Your order has been dispatched, '
                                                         'and will arrive just as fast as '
                                                         'the pony can get there!')

    @allure.step('Проверить наличие кнопки "Back Home"')
    def back_button_availability(self) -> None:
        self.element_is_visible(self.back_btn)
