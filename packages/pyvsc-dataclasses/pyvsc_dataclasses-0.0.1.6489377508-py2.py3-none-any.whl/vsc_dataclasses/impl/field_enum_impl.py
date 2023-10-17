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
from .context import Context

from .ctor import Ctor
from .modelinfo import ModelInfo
from .field_base_impl import FieldBaseImpl


class FieldEnumImpl(FieldBaseImpl):
    
    def __init__(self, name, typeinfo, lib_field):
        super().__init__(name, typeinfo, lib_field)
        ctxt : Context = Ctor.inst().ctxt()
        pass
    
    def get_val(self, lib_obj_p):
        field = lib_obj_p.getField(self._modelinfo._idx)
        val = field.val().val_i()
        val_e = self._modelinfo._typeinfo._e_info.v2e_m[val]
        return val_e
    
    def set_val(self, lib_obj_p, v):
        field = lib_obj_p.getField(self._modelinfo._idx)
        val = self._modelinfo._typeinfo._e_info.e2v_m[v]
        field.val().set_val_i(val)
    
    @property
    def val(self):
        val = self._modelinfo._lib_obj.val().val_i()
        val_e = self._modelinfo._typeinfo._e_info.v2e_m[val]
        return val_e
    
    @val.setter
    def val(self, v):
        val = self._modelinfo._typeinfo._e_info.e2v_m[v]
        self._modelinfo._lib_obj.val().set_val_i(val)
    
