#****************************************************************************
#* extend_randclass_decorator_impl.py
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

import dataclasses
import typeworks

from .context import TypeFieldAttr
from .constraint_decorator_impl import ConstraintDecoratorImpl
from .ctor import Ctor
from .type_kind_e import TypeKindE
from .rand_t import RandT
from .scalar_t import ScalarT
from .typeinfo_extend_randclass import TypeInfoExtendRandClass
from .typeinfo_randclass import TypeInfoRandClass
from .typeinfo_field import TypeInfoField
from .typeinfo_scalar import TypeInfoScalar

class ExtendRandClassDecoratorImpl(typeworks.ClsDecoratorBase):

    def __init__(self, target, args, kwargs):
        super().__init__(args, kwargs)
        self.target = target
        target_ti = typeworks.TypeInfo.get(target, False)
        self.target_ti = TypeInfoRandClass.get(target_ti)
        self.logger.debug("target_ti: %s %s" % (str(target_ti), str(self.target_ti)))
        pass

    def get_type_category(self):
        return TypeKindE.ExtendRandClass

    def _getLibDataType(self, name):
        # Extensions do not have a core-object representation
        return None

    def pre_decorate(self, T):
        # Ensure we've created type-info of appropriate type
        self.logger.debug("ExtendRandClasss.PreDecorate")
        randclass_ti = TypeInfoExtendRandClass.get(self.get_typeinfo())
        ctor = Ctor.inst()
        
        self.logger.debug("  TI: %s" % str(randclass_ti))

#        typename = ctor.pyType2TypeName(T.__qualname__)
#        randclass_ti.lib_typeobj = self._getLibDataType(typename)

        self.logger.debug("RandClass %s" % T.__qualname__)
        self.logger.debug("  Bases: %s" % str(T.__bases__))
        self.logger.debug("  TI: %s ; lib_typeobj: %s" % (str(randclass_ti), str(randclass_ti.lib_typeobj)))

        constraints = typeworks.DeclRgy.pop_decl(ConstraintDecoratorImpl)
        randclass_ti.addConstraints(constraints)
        
        for b in T.__bases__:
            info = typeworks.TypeInfo.get(b, False)
            if info is not None:
                b_randclass_info = TypeInfoRandClass.get(info, False)
                if b_randclass_info is not None:
                    self.__collectConstraints(b_randclass_info, b)        
                
        super().pre_decorate(T)

    def init_annotated_field(self, key, value, has_init, init):
        randclass_ti = TypeInfoExtendRandClass.get(self.get_typeinfo())
        is_rand = False
            
        self.logger.debug("type(value)=%s" % str(type(value)))

        if issubclass(value, RandT):
            self.logger.debug("isrand")
            t = value.T
            is_rand = True
        else:
            t = value

        if issubclass(t, ScalarT):
            ctor = Ctor.inst()
            self.logger.debug("   Is a scalar: %d,%d" % (t.W, t.S))

            if has_init:
                self.logger.debug("Field: %s init=%s" % (key, str(init)))
                iv = ctor.ctxt().mkModelVal()
                iv.setBits(t.W)
                if t.S:
                    iv.set_val_i(init)
                else:
                    iv.set_val_u(init)
            else:
                iv = None
                
            # Create a TypeField instance to represent the field
            it = ctor.ctxt().findDataTypeInt(t.S, t.W)
            if it is None:
                it = ctor.ctxt().mkDataTypeInt(t.S, t.W)
                ctor.ctxt().addDataTypeInt(it)
                        
            attr = TypeFieldAttr.NoAttr
                    
            if is_rand:
                attr |= TypeFieldAttr.Rand

            field_type_obj = ctor.ctxt().mkTypeFieldPhy(
                key,
                it,
                False,
                attr,
                iv) # TODO: initial value

            field_ti = TypeInfoField(key, TypeInfoScalar(t.S))
            randclass_ti.addField(field_ti, field_type_obj)
            self.set_field_initial(key, None)
        elif issubclass(t, ListT):
            self.logger.debug("  Is a list: %s" % str(t.T))
        else:
            raise Exception("Non-scalar fields are not yet supported")

    def decorate(self, T):
        dataclasses.dataclass(T, **self.kwargs)
        return None

    def __collectConstraints(self, typeinfo, clsT):
        """Connect constraints from base classes"""
        # First, connect any additional constraints registered in the base class
        for cn,cd in clsT._typeinfo._constraint_m.items():
            if cn not in typeinfo._constraint_m.keys():
                self.logger.debug("Adding base-class %s" % cn)
                typeinfo._constraint_l.append(cd)
                typeinfo._constraint_m[cn] = cd
            else:
                self.logger.debug("Skipping overridden %s" % cn)
                pass
                
        # Now, keep digging
        for b in clsT.__bases__:
            if hasattr(b, "_typeinfo"):
                self.__collectConstraints(typeinfo, b)

