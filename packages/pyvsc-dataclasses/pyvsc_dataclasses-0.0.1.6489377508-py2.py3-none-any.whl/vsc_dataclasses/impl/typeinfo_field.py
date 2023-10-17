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

import logging
from .typeinfo_vsc import TypeInfoVsc
from .type_kind_e import TypeKindE

class TypeInfoField(object):
    
    def __init__(self, name, typeinfo):
        self.name = name
        self.typeinfo = typeinfo
        self.idx = -1
        self.logger = logging.getLogger(type(self).__name__)

    def createInst(
        self,
        modelinfo_p,
        name,
        idx):
        self.logger.debug("TypeInfoField.createInst: %s" % name)
        if self.typeinfo is None:
            raise Exception("Null TypeInfo for %s" % name)
        return self.typeinfo.createInst(modelinfo_p, name, idx)

