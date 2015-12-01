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

from hamcrest import assert_that, equal_to
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from pages.page import Page
from pages.standard_components.table import Table
from pages.ui_component import UIComponent

PAGE_LOADING_TIMEOUT = 10
POLLING_INTERVAL = 1
LOGIN_PAGE_URL = 'http://the-internet.herokuapp.com/login'

EXPECTED_LABEL_LIST = ['Iuvaret0', 'Apeirian0', 'Adipisci0', 'Definiebas0', 'Consequuntur0', 'Phaedrum0', 'edit delete']


class SampleTableTest(unittest.TestCase):

    def setUp(self):
        self.driver = WebDriver()

    def tearDown(self):
        self.driver.quit()

    def test_can_get_table_elements(self):
        sample_page = SamplePage(self.driver).load().wait_until_loaded()
        first_table_raw_values = sample_page.read_first_table_raw()

        assert_that(first_table_raw_values, equal_to(EXPECTED_LABEL_LIST))


class SamplePage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver, 'sample page')
        self.add_trait(lambda: SampleTable(self.driver).is_present(), 'has table')

    def load(self):
        self.driver.get('http://the-internet.herokuapp.com/challenging_dom')
        return self

    def read_first_table_raw(self):
        table_raws = SampleTable(self.driver).get_items()
        return [i for i in table_raws[0].values()]


class SampleTable(Table):

    def __init__(self, driver):
        super(SampleTable, self).__init__(driver, 'sample table', [By.XPATH, './tbody/tr'], TableRow, 'raw',
                                          [By.XPATH, '//table'])


class TableRow(UIComponent):

    def __init__(self, driver, name):
        super(TableRow, self).__init__(driver, name)

    def values(self):
        return [i.text for i in self.locate().find_elements_by_xpath('./td')]
