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
# Created on Mar 18, 2022
#
# @author: mballance
#****************************************************************************

from typing import List

from .modelinfo import ModelInfo
from .context import ModelBuildContext

from .modelinfo import ModelInfo

from .ctor import Ctor

from .typeinfo_field import TypeInfoField
from .constraint_decl import ConstraintDecl
from .type_kind_e import TypeKindE
from .typeinfo_vsc import TypeInfoVsc

class TypeInfoRandClass(TypeInfoVsc):
    
    def __init__(self, info, kind=TypeKindE.RandClass):
        super().__init__(info, kind)
        self._field_ctor_m = {}
        self._constraint_m = {}
        self._constraint_l = []
        self._field_typeinfo = []
        self._extension_l = []
        self._base_init = None
        
    def init(self, 
        obj, 
        args, 
        kwargs,
        modelinfo=None,
        ctxt_b=None):
        # Run the base behavior
        self._info.init(obj, args, kwargs)
        
        # TODO: Push a context into which to add fields
        ctor = Ctor.inst()

        if ctxt_b is None:
            ctxt_b = ctor.ctxt().mkModelBuildContext(ctor.ctxt())

        if modelinfo is None:
            modelinfo = ModelInfo(obj, "<>", self)

        s = ctor.scope()

        self._logger.debug("s=%s" % str(s))

        ctor.push_raw_mode()

        # Create modelinfo for this field
        obj._modelinfo = modelinfo

        if s is not None:
            if s.facade_obj is None:
                # The field-based caller has setup a frame for us. 
                # Add the object reference
                s.facade_obj = obj
            elif s.facade_obj is obj:
                s.inc_inh_depth()
            else:
                # Need a new scope
                if ctor.is_type_mode():
                    raise Exception("Shouldn't hit this in type mode")
                self._logger.debug("TODO: Create root field for %s" % self.lib_typeobj.name())
                obj._modelinfo.libobj = self.lib_typeobj.mkRootField(ctxt_b, "<>", False)
                obj._randstate = None
                s = ctor.push_scope(obj, obj._modelinfo.libobj, False)
        else:
            # Push a new scope. Know we're in non-type mode
            self._logger.debug("Self: %s" % str(self))
            self._logger.debug("TODO: Create root field for %s" % self.lib_typeobj.name())
            obj._modelinfo.libobj = self.lib_typeobj.mkRootField(ctxt_b, "<>", False)
            obj._randstate = None
            s = ctor.push_scope(obj, obj._modelinfo.libobj, False)

        # Capture the active composite-type scope
        modelinfo.libobj = s.lib_scope

        if not ctor.is_type_mode():
            self._logger.debug("Set Data: %08x" % id(obj))
            if s.lib_scope is not None:
                s.lib_scope.setFieldData(obj)
        
        for field_ti in self.getFields():
            self._logger.debug("name: %s" % field_ti.name)

            # What to pass here?
            
            # Grab the appropriate field from the scope
            self._logger.debug("lib_scope=%s" % str(s.lib_scope))

            # Field constructor responsible for adding itself
            # to the parent modelinfo
            self._logger.debug("field_ti .name=%s .idx: %d" % (field_ti.name, field_ti.idx))
#            self._logger.debug("  getField: %s" % str(s.lib_scope.getField(field_ti.idx)))
            f = field_ti.createInst(
                modelinfo,
                field_ti.name,
                field_ti.idx)

            self._logger.debug("Set Attr: %s=%s" % (field_ti.name, str(f)))
            setattr(obj, field_ti.name, f)
            
#            s.lib_scope.addField(f.model())

        ctor.pop_raw_mode()

        # TODO: determine if we're at leaf level (?)
        # if s.dec_inh_depth() == 0:
        #     if ctor.is_type_mode():
        #         # Time to pop this level. But before we do so, build
        #         # out the relevant constraints
        #         self._logger.debug("-> build out constraints: %s" % str(self.getConstraints()))

        #         # This doesn't seem right...
        #         ctor.push_expr_mode()
        #         for c in self.getConstraints():
        #             cb = ctor.ctxt().mkTypeConstraintBlock(c._name)
        #             ctor.push_constraint_scope(cb)
        #             self._logger.debug("--> Invoke constraint")
        #             c._method_t(obj)
        #             self._logger.debug("<-- Invoke constraint")
        #             ctor.pop_constraint_scope()
                
        #             obj._modelinfo.libobj.addConstraint(cb)
        #         ctor.pop_expr_mode()

        #         self._logger.debug("<- build out constraints: %s" % str(self.getConstraints()))
        #     ctor.pop_scope()

    def createInst(
            self,
            modelinfo_p,
            name,
            idx):
        ctor = Ctor.inst()

        # TODO: need to push a scope with the lib_typeobj for this field
        if self.lib_typeobj is None:
            raise Exception("Type-info for field %s is null" % name)
        ctor.push_scope(None, self.lib_typeobj.getField(idx), True)
        ctor.push_type_mode()
        field = self.info.Tp()
        ctor.pop_type_mode()

        # Back-patch name and index -- something not available inside the constructor
        field._modelinfo.name = name
        field._modelinfo.idx = idx
        modelinfo_p.addSubfield(field._modelinfo)

        return field

    def createTypeInst(self):
        ctor = Ctor.inst()

        ctor.push_scope(None, self.lib_typeobj, True)
        ctor.push_type_mode()
        obj = self.info.Tp()
        ctor.pop_type_mode()

        return obj

    def elab(self, obj):
        # Apply extensions before elaboration
        for e in self._extension_l:
            e.applyExtension(self)
        self.elabConstraints(obj)

    def elabConstraints(self, obj):
        """
        Elaborate constraint types
        """
        ctor = Ctor.inst()

        ctor.push_scope(obj, self.lib_typeobj, True)
        ctor.push_type_mode()
        ctor.push_expr_mode()        
        for c in self.getConstraints():
            cs = ctor.ctxt().mkTypeConstraintBlock(c.name)
            ctor.push_constraint_scope(cs)
            c(obj)
            ctor.pop_constraint_scope()
            self.lib_typeobj.addConstraint(cs)
        ctor.pop_expr_mode()
        ctor.pop_type_mode()
        ctor.pop_scope()

    def addExtension(self, ext):
        self._extension_l.append(ext)

    def addField(self, field_ti, field_obj):
        if field_obj is not None and self._lib_typeobj is not None:
            self._lib_typeobj.addField(field_obj)
        else:
            self._logger.debug("Skip adding field %s" % field_ti.name)
        field_ti.idx = len(self._field_typeinfo)
        self._field_typeinfo.append(field_ti)

    def getField(self, idx):
        return self._field_typeinfo[idx]
        
    def getFields(self) -> List[TypeInfoField]:
        return self._field_typeinfo
        
    def addConstraint(self, c : ConstraintDecl):
        self._constraint_m[c.name] = c
        self._constraint_l.append(c)
        
    def addConstraints(self, c_l : List[ConstraintDecl]):
        for c in c_l:
            self.addConstraint(c)
            
    def getConstraints(self) -> List[ConstraintDecl]:
        return self._constraint_l
        
    @staticmethod
    def get(info) -> 'TypeInfoRandClass':
        if not hasattr(info, TypeInfoVsc.ATTR_NAME):
            setattr(info, TypeInfoVsc.ATTR_NAME, TypeInfoRandClass(info))
        return getattr(info, TypeInfoVsc.ATTR_NAME)

