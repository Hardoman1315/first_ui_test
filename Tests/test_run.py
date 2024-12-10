import allure

from Pages.cart_page import CartPage
from Pages.checkout_page import CheckoutPage
from Pages.inventory_page import InventoryPage
from Pages.login_page import LoginPage


@allure.title('Проверить функциональность корзины')
def test_cart_workability(driver):
    auth_page = LoginPage(driver)

    auth_page.auth('standard_user', 'secret_sauce')

    inv_page = InventoryPage(driver)

    inv_page.add_tshirt_to_cart_btn_click()
    inv_page.cart_badge_number()
    inventory_price = inv_page.cart_btn_click()
    cart_page = CartPage(driver)
    cart_page.tshirt_availability()
    cart_price = cart_page.compare_price()

    assert inventory_price == cart_price, (
        '[FAILED] Prices are different'
    )

    cart_page.checkout_click()

    checkout_page = CheckoutPage(driver)

    checkout_page.fill_fields('Masha', 'Smirnova', '432001')
    checkout_page.tshirt_availability()
    cart_price = checkout_page.compare_price()

    assert inventory_price == cart_price, (
        '[FAILED] Prices are different'
    )

    checkout_page.payment_title()
    checkout_page.payment_card()
    payment_price = checkout_page.payment_price()

    assert inventory_price == payment_price, (
        '[FAILED] prices are different'
    )

    checkout_page.tax()
    checkout_page.finish_button()

    checkout_page.is_checkout_complete()
    checkout_page.is_thank_for_order()
    checkout_page.delivery_text()
    checkout_page.back_button_availability()
