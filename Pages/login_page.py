import allure
from selenium.webdriver.common.by import By
from Pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

    login = (By.ID, 'user-name')           #Локатор по ID для элемента строки ввода login
    password = (By.ID, 'password')         #Локатор по ID для элемента строки ввода password
    login_btn = (By.NAME, 'login-button')  #Локатор по Name для элемента кнопка Login

    @allure.step('Войти в аккаунт')
    def auth(self, login: str, password: str) -> None:
        self.insert_value(self.login, login)
        self.insert_value(self.password, password)
        self.click_element(self.login_btn)

    @allure.step('Ввести логин')
    def insert_login(self, login: str) -> None:
        self.insert_value(self.login, login)

    @allure.step('Ввести пароль"')
    def insert_password(self, password: str) -> None:
        self.insert_value(self.password, password)

    @allure.step('Нажать кнопку "LOGIN"')
    def click_login_button(self) -> None:
        self.click_element(self.login_btn)
