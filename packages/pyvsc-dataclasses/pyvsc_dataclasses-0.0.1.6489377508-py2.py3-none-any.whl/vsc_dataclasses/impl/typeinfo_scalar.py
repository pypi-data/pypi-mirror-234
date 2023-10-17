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
#****************************************************************************
from .ctor import Ctor
from .field_scalar_impl import FieldScalarImpl
from .modelinfo import ModelInfo
from .typeinfo_vsc import TypeInfoVsc


class TypeInfoScalar(TypeInfoVsc):

    def __init__(self, dt):
        super().__init__(None, None)
        if dt is None:
            raise Exception("no data-type object")
        self._lib_typeobj = dt

    @property
    def is_signed(self):
        return self._lib_typeobj.is_signed()

    def createInst(
            self,
            modelinfo_p : ModelInfo,
           name, 
           idx):
        ctor = Ctor.inst()
        field = FieldScalarImpl(name, self, idx)

        # Get the appropriate type/inst object
        if not ctor.is_type_mode():
            field._modelinfo.libobj = modelinfo_p.libobj.getField(idx)

        modelinfo_p.addSubfield(field._modelinfo)
        return field
    
    def init2Val(self, init):
        return Ctor.inst().ctxt().mkValRefInt(
            init, 
            self._lib_typeobj.is_signed(), 
            self._lib_typeobj.width())
