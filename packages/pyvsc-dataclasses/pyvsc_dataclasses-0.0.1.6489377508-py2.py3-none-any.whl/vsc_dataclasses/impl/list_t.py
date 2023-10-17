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
# Created on Jun 28, 2022
#
# @author: mballance
#****************************************************************************
import typing

from .ctor import Ctor
from .enum_t import EnumT
from .field_list_object_impl import FieldListObjectImpl
from .field_list_scalar_impl import FieldListScalarImpl
from .list_tt_meta import ListTTMeta
from .scalar_t import ScalarT
from .type_kind_e import TypeKindE
from .typeinfo_vsc import TypeInfoVsc


class ListT(object):
    T = None
    DIM = []
    
    def __new__(cls,
                t,
                sz=0,
                is_rand=False,
                is_randsz=False,
                init=None):
        ctor = Ctor.inst()

        lib_type = None
        typeinfo = None
        kind = None
        if hasattr(t, "_modelinfo"):
            print("Is instance -- no type")
            typeinfo = t._modelinfo._typeinfo
            kind = t._modelinfo._typeinfo._kind
            lib_type = t._modelinfo._typeinfo._lib_typeobj
        elif hasattr(t, "_typeinfo"):
            print("Is user-defined type")
            
        print("kind: %s" % kind)

        # if True:
        #     if issubclass(t, ScalarT):
        #         print("Scalar")
        #     elif issubclass(t, EnumT):
        #         print("Enum")
        #     elif hasattr(t, "_typeinfo"):
        #         print("User-defined type")
        #     else:
        #         raise Exception("Type \"%s\" is not a recognized VSC type" % str(type(t)))
        # else:
        #     print("non-type class")
        
        lib_field = ctor.ctxt().mkModelFieldVecRoot(
            lib_type,
            "")
        
        if kind == TypeKindE.Scalar:
            ret = FieldListScalarImpl(
                "", 
                TypeInfoVsc(TypeKindE.List, None, typeinfo),
                lib_field)
        elif kind == TypeKindE.Enum:
            pass
        elif kind == TypeKindE.RandObj:
            ret = FieldListObjectImpl(
                "", 
                TypeInfoVsc(TypeKindE.List, None, typeinfo),
                lib_field)
        
        
        return ret
    