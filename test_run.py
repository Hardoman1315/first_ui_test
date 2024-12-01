import allure

from pages import LoginPage, InventoryPage, ItemPage, CartPage

@allure.title('Проверить корректность добавления товаров в корзину')
def test_est_1_login(driver):
    auth_page = LoginPage(driver)
    with allure.step('Войти в аккаунт'):
        auth_page.auth('standard_user', 'secret_sauce')

    inventory_page = InventoryPage(driver)
    with allure.step('Выбрать товар'):
        inventory_page.choose_item()

    item_page = ItemPage(driver)
    with allure.step('Нажать кнопку "Add to cart"'):
        item_page.add_to_cart_btn_click()
    with allure.step('Нажать кнопку "Back to products'):
        item_page.return_to_products()

    with allure.step('Нажать на "Sauce Labs Fleece Jacket"'):
        inventory_page.add_jacket_to_cart_btn_click()
    with allure.step('Нажать на кнопку корзины'):
        inventory_page.cart_btn_click()

    cart_page = CartPage(driver)
    with allure.step('Проверить что в корзину добавилось оба предмета'):
        assert cart_page.number_of_products() == 2

@allure.title('Проверить авторизацию с корректными данными входа')
def test_auth(driver):
    auth_page = LoginPage(driver)
    with allure.step('Ввести корректный логин'):
        auth_page.input_login('standard_user')
    with allure.step('Ввести корректный пароль'):
        auth_page.input_password('secret_sauce')
    with allure.step('Нажать кнопку "Login"'):
        auth_page.login_button_click()

    with allure.step('Проверить корректный переход на страницу магазина'):
        assert InventoryPage(driver).check_inventory_page_open(), (
            '[FAILED] Login attempt was failed, check login and password'
        )

@allure.title('Проверить авторизацию с некорректными данными входа')
def test_invalid_auth(driver):
    auth_page = LoginPage(driver)
    with allure.step('Ввести корректный логин'):
        auth_page.input_login('standard_user')
    with allure.step('Ввести некорректный пароль'):
        auth_page.input_password('123')
    with allure.step('Нажать кнопку "Login"'):
        auth_page.login_button_click()

    with allure.step('Проверить невозможность перехода при некорректных данных'):
        assert not InventoryPage(driver).check_inventory_page_open(), (
            '[FAILED] Login attempt was not failed with incorrect login and/or password'
        )
