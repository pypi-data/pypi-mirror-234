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

from .ctor import Ctor
from .field_scalar_impl import FieldScalarImpl
from .type_kind_e import TypeKindE
from .typeinfo_vsc import TypeInfoVsc


class ScalarT(object):
    W = 0
    S = False
    
    def __new__(cls, w=-1, i=0):
        ctor = Ctor.inst()
        
        # TODO: need to check construction mode, etc?

        if w == -1:
            w = cls.W 
        
        # Create a model field based on the relevant signedness/size
        print("ScalarT: w=%d, cls.W=%d" % (w, cls.W))
        lib_type = ctor.ctxt().findDataTypeInt(cls.S, w)
        if lib_type is None:
            lib_type = ctor.ctxt().mkDataTypeInt(cls.S, w)
            ctor.ctxt().addDataTypeInt(lib_type)
            
        
        lib_field = ctor.ctxt().mkModelFieldRoot(
            lib_type,
            "")
        
        if cls.W <= 64:
            if cls.S:
                lib_field.val().set_val_i(i)
            else:
                lib_field.val().set_val_u(i)
        else:
            raise Exception("Field >64 not yet supported")

        print("scalar_t::new")        
        ret = FieldScalarImpl(
            "", 
            TypeInfoVsc(TypeKindE.Scalar, lib_type),
            lib_field, 
            cls.S)
        
        return ret
    
    # def __init__(self, name="", i=0):
    #     ctor = Ctor.inst()
    #
    #     # TODO: need to check construction mode, etc?
    #
    #     # Create a model field based on the relevant signedness/size
    #     lib_type = ctor.ctxt().findDataTypeInt(type(self).S, type(self).W)
    #     if lib_type is None:
    #         lib_type = ctor.ctxt().mkDataTypeInt(type(self).S, type(self).W)
    #         ctor.ctxt().addDataTypeInt(lib_type)
    #
    #
    #     lib_field = ctor.ctxt().mkModelFieldRoot(
    #         lib_type,
    #         name)
    #
    #     if type(self).W <= 64:
    #         if type(self).S:
    #             lib_field.val().set_val_i(iv)
    #         else:
    #             lib_field.val().set_val_u(iv)
    #     else:
    #         raise Exception("Field >64 not yet supported")
    #
    #     super().__init__(name, lib_field, type(self).S)

    # @classmethod
    # def createField(cls, name, is_rand, iv):
    #     print("ScalarT::create %d %d iv=%s" % (cls.W, cls.S, str(iv)))
    #     ret = FieldScalarImpl(name, cls.W, cls.S, is_rand, iv)
    #     return ret
    