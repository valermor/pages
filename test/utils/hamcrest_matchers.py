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
from hamcrest.core.base_matcher import BaseMatcher
from selenium.common.exceptions import TimeoutException

from pages.page import Page

DEFAULT_POLLING_TIME = 0.5
DEFAULT_TIMEOUT = 25


class PageIsLoaded(BaseMatcher):

    def __init__(self, timeout):
        BaseMatcher.__init__(self)
        self.timeout = timeout
        self.polling = DEFAULT_POLLING_TIME
        self.page_name = None

    def _matches(self, page):
        self.page_name = page.name
        if isinstance(page, Page):
            try:
                page.wait_until_loaded(self.timeout, self.polling)
                return True
            except TimeoutException:
                return False

    def describe_to(self, description):
        description.append_text("Expected page {0} to load within {1} ms".format(self.page_name, str(self.timeout)))

    def describe_mismatch(self, item, mismatch_description):
            mismatch_description.append_text('page load timed out.')

    def with_timeout(self, timeout):
        self.timeout = timeout
        return self

    def with_polling(self, polling):
        self.polling = polling
        return self


def is_loaded(timeout=30):
    return PageIsLoaded(timeout)
