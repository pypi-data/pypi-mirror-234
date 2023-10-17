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
import typeworks
from typeworks.impl.typeinfo import TypeInfo
from .typeinfo_scalar import TypeInfoScalar
from .type_utils import TypeUtils
from .constraint_decorator_impl import ConstraintDecoratorImpl

from .scalar_t import ScalarT
from .context import TypeFieldAttr
from .ctor import Ctor
from .typeinfo_randclass import TypeInfoRandClass
from .randclass_impl import RandClassImpl
from .type_kind_e import TypeKindE
from .typeinfo_field import TypeInfoField
from .rand_t import RandT
from .list_t import ListT
from .typeinfo_vsc import TypeInfoVsc

class RandClassDecoratorImpl(typeworks.ClsDecoratorBase):
    """Decorator implementation for @randclass and type-model building code"""
    
    def __init__(self, args, kwargs):
        super().__init__(args, kwargs)
        
    def get_type_category(self):
        return TypeKindE.RandClass
    
    def _getLibDataType(self, name):
        ctor = Ctor.inst()

        ds_t = ctor.ctxt().findDataTypeStruct(name)
        
        if ds_t is not None:
            raise Exception("Type already registered")
        else:
            ds_t = ctor.ctxt().mkDataTypeStruct(name)
            ctor.ctxt().addDataTypeStruct(ds_t)
        
        return ds_t
    
    def pre_decorate(self, T):
        # Ensure we've created type-info of appropriate type
        self.logger.debug("RandClasss.PreDecorate")
        randclass_ti = TypeInfoRandClass.get(self.get_typeinfo())
        ctor = Ctor.inst()
        
        self.logger.debug("  TI: %s" % str(randclass_ti))

        typename = ctor.pyType2TypeName(T.__qualname__)
        randclass_ti.lib_typeobj = self._getLibDataType(typename)

        self.logger.debug("RandClass %s" % T.__qualname__)
        self.logger.debug("  Bases: %s" % str(T.__bases__))
        self.logger.debug("  TI: %s ; lib_typeobj: %s" % (str(randclass_ti), str(randclass_ti.lib_typeobj)))

        constraints = typeworks.DeclRgy.pop_decl(ConstraintDecoratorImpl)
        randclass_ti.addConstraints(constraints)
        
        for b in T.__bases__:
            info = typeworks.TypeInfo.get(b, False)
            if info is not None:
                b_randclass_info = TypeInfoRandClass.get(info)
                if b_randclass_info is not None:
                    self.__collectConstraints(b_randclass_info, b)        
                
        super().pre_decorate(T)
        
    def init_annotated_field(self, key, value, has_init, init):
        ctor = Ctor.inst()
        randclass_ti = TypeInfoRandClass.get(self.get_typeinfo())
            
        self.logger.debug("type(value)=%s" % str(type(value)))
        is_rand = False
        if issubclass(value, RandT):
            self.logger.debug("isrand")
            value = value.T
            is_rand = True

        ti = TypeUtils().val2TypeInfo(value)

        attr = TypeFieldAttr.NoAttr

        if has_init:
            self.logger.debug("Field: %s init=%s" % (key, str(init)))
            iv = ti.init2Val(init)
        else:
            iv = None
                   
        if is_rand:
            attr |= TypeFieldAttr.Rand

        field_type_obj = ctor.ctxt().mkTypeFieldPhy(
            key,
            ti._lib_typeobj,
            False,
            attr,
            iv) # TODO: initial value

        field_ti = TypeInfoField(key, ti)
        randclass_ti.addField(field_ti, field_type_obj)
        self.set_field_initial(key, None)

    def _process_scalar_field(self, t, key, is_rand, has_init, init):
        ctor = Ctor.inst()
        randclass_ti = TypeInfoRandClass.get(self.get_typeinfo())

        self.logger.debug("   Is a scalar: %d,%d" % (t.W, t.S))

        if has_init:
            self.logger.debug("Field: %s init=%s" % (key, str(init)))
            iv = ctor.ctxt().mkValRefInt(init, t.S, t.W)
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

    def _process_list_field(self, t, key, is_rand, has_init, init):
        ctor = Ctor.inst()
        randclass_ti = TypeInfoRandClass.get(self.get_typeinfo())

        inner_t = t.T

        print("DIM: %s" % str(t.DIM))

        # Find the inner type
        if issubclass(inner_t, ScalarT):
            print("Inner type is scalar")
            t_obj = ctor.ctxt().findDataTypeInt(inner_t.S, inner_t.W)
            if t_obj is None:
                t_obj = ctor.ctxt().mkDataTypeInt(inner_t.S, inner_t.W)
            ctor.ctxt().addDataTypeInt(t_obj)
            ti = TypeInfoScalar(inner_t.S)
        elif issubclass(inner_t, ListT):
            print("Inner type is a list")
            self._process_list_field(t, key, is_rand, has_init, init)
        else:
            print("Inner type is a class")

            cls_ti_t = TypeInfo.get(inner_t, False)

            if cls_ti_t is None:
                raise Exception("Type %s is not a VSC type" % str(t))

            cls_ti = TypeInfoRandClass.get(cls_ti_t)
            t_obj = cls_ti._lib_typeobj
            ti = cls_ti

          

        self.logger.debug("   Is a RandClass Type")

        if has_init:
            self.logger.debug("Field: %s init=%s" % (key, str(init)))
            iv = ctor.ctxt().mkValRefInt(init, t.S, t.W)
        else:
            iv = None
                
        # Create a TypeField instance to represent the field
        attr = TypeFieldAttr.NoAttr
                   
        if is_rand:
            attr |= TypeFieldAttr.Rand

        field_type_obj = ctor.ctxt().mkTypeFieldPhy(
            key,
            t_obj,
            False,
            attr,
            iv) # TODO: initial value

        field_ti = TypeInfoField(key, ti)
        randclass_ti.addField(field_ti, field_type_obj)
        self.set_field_initial(key, None)            
    
    def _process_class_field(self, t, key, is_rand, has_init, init):
        ctor = Ctor.inst()
        randclass_ti = TypeInfoRandClass.get(self.get_typeinfo())

        cls_ti_t = TypeInfo.get(t, False)

        if cls_ti_t is None:
            raise Exception("Type %s is not a VSC type" % str(t))
          
        cls_ti = TypeInfoRandClass.get(cls_ti_t)

        self.logger.debug("   Is a RandClass Type")

        if has_init:
            self.logger.debug("Field: %s init=%s" % (key, str(init)))
            iv = ctor.ctxt().mkValRefInt(init, t.S, t.W)
        else:
            iv = None
                
        # Create a TypeField instance to represent the field
        attr = TypeFieldAttr.NoAttr
                   
        if is_rand:
            attr |= TypeFieldAttr.Rand

        field_type_obj = ctor.ctxt().mkTypeFieldPhy(
            key,
            cls_ti._lib_typeobj,
            False,
            attr,
            iv) # TODO: initial value

        field_ti = TypeInfoField(key, cls_ti)
        randclass_ti.addField(field_ti, field_type_obj)
        self.set_field_initial(key, None)            

    def _get_type(self, t, level=0):
        # Returns: is_rand,lib_obj,type_info
        is_rand : bool = False

        if level == 0 and issubclass(t, RandT):
            self.logger.debug("isrand")
            t = t.T
            is_rand = True

        if issubclass(t, ScalarT):
            ctor = Ctor.inst()
            dt = ctor.ctxt().findDataTypeInt(t.S, t.W)
            if dt is None:
                dt = ctor.ctxt().mkDataTypeInt(t.S, t.W)
                ctor.ctxt().addDataTypeInt(dt)
            return (is_rand, dt, TypeInfoScalar(t.S))
        elif issubclass(t, ListT):
            print("List")
            ctor = Ctor.inst()
            # Construct single nested type description for
            # descriptions of both forms
            list_dim = []
            is_rand, obj_t, ti_t = self._get_type(t.T)

            if len(t.DIM) > 0:
                # Fixed-size dimensions
                print("have DIM")
                for sz in t.DIM[::-1]:
                    print("sz: %d" % sz)
                    # create a fixed-size list type 
                    # of the inner-type kind
                    list_obj_t = ctor.ctxt().findDataTypeListFixedSize(obj_t, sz)
                    obj_t = list_obj_t
            else:
                obj_t = ctor.ctxt().findDataTypeList(obj_t)
            
            return (is_rand, obj_t, ti_t)
        else:
            ctor = Ctor.inst()

            cls_ti_t = TypeInfo.get(t, False)

            if cls_ti_t is None:
                raise Exception("Type %s is not a VSC type" % str(t))

            randclass_ti = TypeInfoRandClass.get(cls_ti_t)
            return (is_rand, randclass_ti._lib_typeobj, randclass_ti)
        


    def _get_list_dimensions(self, list_t, dim):
        t = list_t.T

        # Find the inner type
        if issubclass(t, ScalarT):
            ctor = Ctor.inst()
            print("DIM: %s" % str(list_t.DIM))
            print("Inner type is scalar")
            t_obj = ctor.ctxt().findDataTypeInt(t.S, t.W)
            if t_obj is None:
                t_obj = ctor.ctxt().mkDataTypeInt(t.S, t.W)
            ctor.ctxt().addDataTypeInt(t_obj)
            ti = TypeInfoScalar(t.S)
            if len(list_t.DIM) > 0:
                for dim_sz in list_t.DIM:
                    dim.append((t_obj, ti, dim_sz))
            else:
                dim.append((t_obj, ti, -1))
        elif issubclass(t, ListT):
            print("Inner type is a list")
#            self._process_list_field(t, key, is_rand, has_init, init)
        else:
            print("Inner type is a class")

            cls_ti_t = TypeInfo.get(t, False)

            if cls_ti_t is None:
                raise Exception("Type %s is not a VSC type" % str(t))

            cls_ti = TypeInfoRandClass.get(cls_ti_t)
            t_obj = cls_ti._lib_typeobj
            ti = cls_ti
            if len(list_t.DIM) > 0:
                for dim_sz in list_t.DIM:
                    dim.append((t_obj, ti, dim_sz))
            else:
                dim.append((t_obj, ti, -1))

    
    def post_decorate(self, T, Tp):
        randclass_ti = TypeInfoRandClass.get(self.get_typeinfo())
        super().post_decorate(T, Tp)
        
        # Add methods
        randclass_ti._base_init = Tp.__init__
        RandClassImpl.addMethods(Tp)
        

    def pre_register(self):
        # Finish elaborating the type object by building out the constraints
        # We first must create a temp object that can be used by the constraint builder

        self.elab_type()

    def elab_type(self):
        randclass_ti = TypeInfoRandClass.get(self.get_typeinfo())
        obj = self.create_type_inst()
        randclass_ti.elab(obj)

    def create_type_inst(self):
        """
        Creates the object instance used for type elaboration
        """
        ctor = Ctor.inst()
        randclass_ti = TypeInfoRandClass.get(self.get_typeinfo())

        # Push a frame for the object to find
        self.logger.debug("create_type: lib_typeobj=%s" % str(randclass_ti.lib_typeobj))
        ctor.push_scope(None, randclass_ti.lib_typeobj, True)
        
        # Now, go create the object itself. Note that we're in
        # type mode, so type fields are built out
        obj = self.get_typeinfo().Tp()

        # Note: creation of the object pops the stack frame we pushed

        return obj

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

