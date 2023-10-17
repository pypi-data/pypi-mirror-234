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
# Created on May 25, 2022
#
# @author: mballance
#****************************************************************************
from typing import Dict
from .enum_info import EnumInfo

class EnumInfoMgr(object):
    
    _inst = None
    
    def __init__(self):
        self._enum_info_m = {}
        pass
    
    def getInfo(self, e_t):
        if e_t in self._enum_info_m.keys():
            return self._enum_info_m[e_t]
        else:
            info = EnumInfo(e_t)
            self._enum_info_m[e_t] = info
            return info
    
    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = cls()
        return cls._inst
    
    