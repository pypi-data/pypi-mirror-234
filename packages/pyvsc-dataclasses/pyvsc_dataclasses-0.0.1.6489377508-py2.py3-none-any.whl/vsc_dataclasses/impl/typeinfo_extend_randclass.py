#****************************************************************************
#* type_info_extend_rand_class.py
#*
#* Copyright 2022 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#* Created on:
#*     Author: 
#*
#****************************************************************************

from .typeinfo_vsc import TypeInfoVsc
from .typeinfo_randclass import TypeInfoRandClass
from .type_kind_e import TypeKindE

class TypeInfoExtendRandClass(TypeInfoRandClass):

    def __init__(self, info, kind=TypeKindE.ExtendRandClass):
        super().__init__(info, kind)
        self._fields = []

    def addField(self, field_ti, field_obj):
        self._fields.append((field_ti, field_obj))

    def applyExtension(self, target):
        for f_ti, f_obj in self._fields:
            target.addField(f_ti, f_obj)
        for c in self.getConstraints():
            target.addConstraint(c)

        pass

    @staticmethod
    def get(info) -> 'TypeInfoExtendRandClass':
        if not hasattr(info, TypeInfoVsc.ATTR_NAME):
            setattr(info, TypeInfoVsc.ATTR_NAME, TypeInfoExtendRandClass(info))
        return getattr(info, TypeInfoVsc.ATTR_NAME)

    pass

