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
from hamcrest.core.matcher import Matcher


class IsSameElement(BaseMatcher):

    def __init__(self, equals):
        self.object = equals

    def _matches(self, item):
        return item.is_equal_to(self.object)

    def describe_to(self, description):
        nested_matcher = isinstance(self.object, Matcher)
        if nested_matcher:
            description.append_text('<')
        description.append_description_of(self.object)
        if nested_matcher:
            description.append_text('>')


def same_element_as(obj):
    """Matches if MockedWebElement is equal to a given object."""
    return IsSameElement(obj)
