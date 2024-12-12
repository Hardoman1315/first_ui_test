import allure
from selenium.webdriver.common.by import By
from Pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        self.login = (By.ID, 'user-name')           #Локатор по ID для элемента строки ввода login
        self.password = (By.ID, 'password')         #Локатор по ID для элемента строки ввода password
        self.login_btn = (By.NAME, 'login-button')  #Локатор по Name для элемента кнопка Login

    @allure.step('Войти в аккаунт')
    def auth(self, login: str, password: str) -> None:
        self.find_element(*self.login).send_keys(login)
        self.find_element(*self.password).send_keys(password)
        self.find_element(*self.login_btn).click()

    @allure.step(r'Ввести логин')
    def input_login(self, login: str) -> None:
        self.find_element(*self.login).send_keys(login)

    @allure.step(r'Ввести пароль"')
    def input_password(self, password: str) -> None:
        self.find_element(*self.password).send_keys(password)

    @allure.step(r'Нажать кнопку "LOGIN"')
    def login_button_click(self) -> None:
        self.find_element(*self.login_btn).click()
