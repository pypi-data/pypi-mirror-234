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
# Created on Jul 4, 2022
#
# @author: mballance
#****************************************************************************

from .field_base_impl import FieldBaseImpl
from .ctor import Ctor
from .expr import Expr


class FieldListScalarImpl(FieldBaseImpl):
    
    def __init__(self, name, typeinfo, lib_field):
        super().__init__(name, typeinfo, lib_field)
        
    @property
    def size(self):
        ctor = Ctor.inst()
        
        if ctor.expr_mode():
            if ctor.is_type_mode():
                raise Exception("size")
            else:
                ref = ctor.ctxt().mkModelExprFieldRef(self._modelinfo._lib_obj.getSizeRef())
            return Expr(ref)
        else:
            return self._modelinfo._lib_obj.getSize()
    
    def append(self, v):
        pass
    
    def __getitem__(self, it):
        pass
        