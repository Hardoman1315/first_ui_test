import time

from pages import BasePage, LoginPage, InventoryPage, ItemPage, CartPage


def test_est_1_login(driver):
    auth_page = LoginPage(driver)
    auth_page.auth('standard_user', 'secret_sauce')

    time.sleep(2)

    inventory_page = InventoryPage(driver)
    inventory_page.choose_item()

    time.sleep(2)

    item_page = ItemPage(driver)
    item_page.add_to_cart_btn_click()
    item_page.return_to_products()

    time.sleep(2)

    inventory_page.add_jacket_to_cart_btn_click()
    inventory_page.cart_btn_click()

    time.sleep(2)

    cart_page = CartPage(driver)
    assert cart_page.number_of_products() == 2

    time.sleep(5)
