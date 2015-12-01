############################################################################
# Copyright 2015 Skyscanner Ltd                                            #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#    http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################
import unittest

from hamcrest import assert_that
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from pages.exceptions import NotLoadablePageException
from pages.page import Page
from pages.standard_components.button import Button
from pages.standard_components.textinput import TextInput
from test.utils.hamcrest_matchers import is_loaded


PAGE_LOADING_TIMEOUT = 10
POLLING_INTERVAL = 1
LOGIN_PAGE_URL = 'http://the-internet.herokuapp.com/login'


class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = WebDriver()

    def tearDown(self):
        self.driver.quit()

    def test_can_login(self):
        login_page = LoginPage(self.driver).load().wait_until_loaded()

        secure_area_page = login_page.login_user('tomsmith', 'SuperSecretPassword!')

        assert_that(secure_area_page, is_loaded().with_timeout(PAGE_LOADING_TIMEOUT)
                    .with_polling(POLLING_INTERVAL))


class LoginPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver, 'Login page')
        self.add_trait(self._has_username_input, 'has username')
        self.add_trait(self._has_password_input, 'has password')
        self.add_trait(self._has_submit_button, 'has submit button')

    def load(self):
        self.driver.get(LOGIN_PAGE_URL)
        return self

    def login_user(self, username, password):
        self._user_name().input_text(username)
        self._password().input_text(password)
        self._submit_button().click()
        return SecureAreaPage(self.driver)

    def _has_username_input(self):
        return self._user_name().is_present()

    def _has_password_input(self):
        return self._password().is_present()

    def _has_submit_button(self):
        return self._submit_button().is_present()

    def _user_name(self):
        return TextInput(self.driver, 'username', [By.ID, 'username'])

    def _password(self):
        return TextInput(self.driver, 'password', [By.ID, 'password'])

    def _submit_button(self):
        return Button(self.driver, 'submit', [By.XPATH, "//button[@type = 'submit']"])


class SecureAreaPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver, 'Secure area page')
        self.add_trait(self._has_logout_button, 'has logout button')

    def load(self):
        raise NotLoadablePageException('{0} cannot be loaded'.format(self.name))

    def _has_logout_button(self):
        return Button(self.driver, 'logout', [By.XPATH, "//a[@href='/logout']"]).is_present()
