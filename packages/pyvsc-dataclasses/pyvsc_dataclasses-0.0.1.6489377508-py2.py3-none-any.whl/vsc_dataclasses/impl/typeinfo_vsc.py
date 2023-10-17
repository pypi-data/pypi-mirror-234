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
# Created on Apr 6, 2022
#
# @author: mballance
#****************************************************************************

import typeworks
import logging
from .modelinfo import ModelInfo

class TypeInfoVsc(object):
    
    ATTR_NAME = "_vsc_typeinfo"
    
    def __init__(self, info, kind, inner=None):
        self._info = info
        self._kind = kind
        self._lib_typeobj = None
        self._inner = inner
        self._logger = logging.getLogger(type(self).__name__)

    def createInst(
        self,
        modelinfo_p : ModelInfo, # Parent model info
        name, # Name, just for interest sake
        idx): # Index within the parent native object
        raise NotImplementedError("createInst not implemented for type-info %s" % str(type(self)))
    
    @property
    def lib_typeobj(self):
        return self._lib_typeobj
    
    @lib_typeobj.setter
    def lib_typeobj(self, val):
        self._lib_typeobj = val
        
    @property
    def info(self):
        return self._info
    
    def init2Val(self, init):
        raise NotImplementedError("init2Val not implemented for %s" % str(type(self)))
    
