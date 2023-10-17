#****************************************************************************
# Copyright 2019-2022 Matthew Ballance and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Created on Feb 26, 2022
#
# @author: mballance
#****************************************************************************
from .scalar_t import ScalarT


class IntTMeta(type):
    """Meta-class for int_t types. Generates a unique int_t for each unique width"""
    
    def __init__(self, name, bases, dct):
        self.type_m = {}
        
    def __getitem__(self, item):
        if item in self.type_m.keys():
            return self.type_m[item]
        else:
            t = type("int_t[%d]" % item, (ScalarT,), {})
            t.W = item
            t.S = True
            self.type_m[item] = t
            return t
        