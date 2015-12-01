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
import random
import time

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

DEFAULT_VALUE_PREFIX = '0.253985061310'


class MockedRemoteConnection(object):
    def __init__(self):
        self.expected_commands = []
        self.session_id = random.randint(1, 10000)
        self.element_prefix = u''
        self.dom_elements = []

    def execute(self, command, params):
        for expected_command in self.expected_commands:
            if expected_command['command'] == command:
                for k, v in expected_command['params'].iteritems():
                    if k in params.keys() and v in params.values():
                        expected_command['fulfilled'] = True
        if command == Command.NEW_SESSION:
            return {'value': {}, 'sessionId': self.session_id}

        if command == Command.FIND_CHILD_ELEMENTS or command == Command.FIND_ELEMENTS:
            return_value = []
            for element in self.dom_elements:
                if element['locator'][0] == params['using'] and element['locator'][1] == params['value'] \
                        and self.get_element_value_from_locator(element['parent']) == params['id']:
                    return_value.append({'ELEMENT': element['value']})
            return {'success': 0, 'value': return_value, 'sessionId': self.session_id}

        if command == Command.FIND_CHILD_ELEMENT or command == Command.FIND_ELEMENT:
            for element in self.dom_elements:
                if element['locator'][0] == params['using'] and element['locator'][1] == params['value']:
                    return {'success': 0, 'value': {'ELEMENT': element['value']}, 'sessionId': self.session_id}

        if command == Command.CLICK_ELEMENT:
            return {'sessionId': self.session_id, 'value': None, 'status': 0}

        if command == Command.MOVE_TO:
            return {'sessionId': self.session_id, 'value': None, 'status': 0}

        if command == Command.GET_ELEMENT_TEXT:
            element = self.get_element_from_value(params['id'])
            return {'success': 0, 'value': element['return']['text'], 'sessionId': self.session_id}

        if command == Command.GET_ELEMENT_ATTRIBUTE:
            element = self.get_element_from_value(params['id'])
            attributes_dict = element['return']['name'][params['name']]
            return {'success': 0, 'value': attributes_dict, 'sessionId': self.session_id}

        if command == Command.GET_ACTIVE_ELEMENT:
            return {'success': 0, 'value': {'ELEMENT': self.dom_elements[0]['value']}, 'sessionId': self.session_id}
        if command == Command.SEND_KEYS_TO_ELEMENT:
            return {'success': 0, 'value': None, 'sessionId': self.session_id}

        else:
            return {'success': 0, 'value': None, 'sessionId': self.session_id}

    def set_expected_command(self, command, params=None):
        self.expected_commands.append({'command': command, 'params': params, 'fulfilled': False})

    def set_element_prefix(self, prefix):
        self.element_prefix = prefix

    def set_dom_element(self, locator, value, parent_id=None, return_values=None):
        self.dom_elements.append({'locator': locator, 'value': value, 'parent': parent_id, 'return': return_values})

    def reset_dom_elements(self):
        self.dom_elements = []

    def get_element_value_from_locator(self, locator, position=1):
        return_elements = []
        for element in self.dom_elements:
            if element['locator'][0] == locator[0] and element['locator'][1] == locator[1]:
                return_elements.append(element['value'])
        if len(return_elements) > 0:
            return return_elements[position - 1]
        else:
            return ValueError('found no element with locator {0}'.format(locator))

    def get_element_from_value(self, value):
        for element in self.dom_elements:
            if element['value'] == value:
                return element

    def get_unfulfilled_list(self):
        return filter(lambda x: not x['fulfilled'], self.expected_commands)


class MockedWebDriver(WebDriver):
    def __init__(self, browser_profile=None,
                 proxy=None, keep_alive=False):
        mocked_command_executor = MockedRemoteConnection()
        super(MockedWebDriver, self).__init__(mocked_command_executor, DesiredCapabilities.FIREFOX, browser_profile,
                                              proxy,
                                              keep_alive)
        self.command_executor = mocked_command_executor

    def set_expected_command(self, expected_command, expected_params=None):
        self.command_executor.set_expected_command(expected_command, expected_params)

    def has_fulfilled_expectations(self):
        unfulfilled_list = self.command_executor.get_unfulfilled_list()
        return len(unfulfilled_list) == 0

    def set_element_prefix(self, prefix):
        self.command_executor.set_element_prefix(prefix)

    def set_dom_elements(self, elements):
        """
        Generates ids to be returned by the mocked driver.
        Given elements are those element we expect to locate in the tests.
        """
        for element in elements:
            self.command_executor.set_dom_element(element, generate_value())

    def set_dom_element(self, locator, parent_id=None, children=0, return_values=None):
        if not parent_id and return_values:
            self.command_executor.set_dom_element(locator, generate_value(), return_values=return_values[0])
        elif not parent_id and not return_values:
            self.command_executor.set_dom_element(locator, generate_value())
        else:
            if return_values and not isinstance(return_values, list):
                raise ValueError('return values should be a list')
            for i in range(0, children):
                if return_values:
                    self.command_executor.set_dom_element(locator, generate_value(), parent_id, return_values[i])
                else:
                    self.command_executor.set_dom_element(locator, generate_value(), parent_id)

    def reset_dom_elements(self):
        self.command_executor.reset_dom_elements()

    def get_id_for_stored_element(self, locator, position=1):
        """
        :param position: 1-based position
        """
        return self.command_executor.get_element_value_from_locator(locator, position)


class MockedWebElement(WebElement):
    def __init__(self, parent, id_):
        super(MockedWebElement, self).__init__(parent, id_)
        self._random_id = random.randint(1, 10000)

    def is_equal_to(self, element):
        if isinstance(element, MockedWebElement):
            return element._random_id == self._random_id
        else:
            raise TypeError('expected MockedWebElement, received ' + element.__class__.__name__)

    def __str__(self):
        return "MockedWebElement with id: {id}".format(id=self._random_id)


def generate_value():
    time.sleep(0.2)  # hacky trick to delay generation of random value.
    random.seed(time.time())
    return unicode(DEFAULT_VALUE_PREFIX + str(random.randint(0, 100)))
