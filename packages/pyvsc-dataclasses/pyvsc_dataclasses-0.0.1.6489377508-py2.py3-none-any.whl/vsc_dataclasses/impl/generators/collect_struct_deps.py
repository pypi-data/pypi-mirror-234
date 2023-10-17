#****************************************************************************
#* collect_struct_deps.py
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
import io
import toposort
from vsc_dataclasses.impl.pyctxt.data_type_int import DataTypeInt
from vsc_dataclasses.impl.pyctxt.data_type_struct import DataTypeStruct
from vsc_dataclasses.impl.pyctxt.type_constraint_block import TypeConstraintBlock
from vsc_dataclasses.impl.pyctxt.type_constraint_expr import TypeConstraintExpr
from vsc_dataclasses.impl.pyctxt.type_expr_bin import TypeExprBin
from vsc_dataclasses.impl.pyctxt.type_expr_field_ref import TypeExprFieldRef
from vsc_dataclasses.impl.pyctxt.type_field import TypeField
from vsc_dataclasses.impl.pyctxt.type_field_phy import TypeFieldPhy
from ..context import BinOp
from ..pyctxt.data_type_struct import DataTypeStruct
from ..pyctxt.visitor_base import VisitorBase

class CollectStructDeps(VisitorBase):

    def __init__(self, ctxt):
        self._dep_m = {}
        self._entries = []
        self._entry_m = {}
        self._scope_s = []
        pass

    def collect(self, t : DataTypeStruct):
        self._init()
        t.accept(self)
        return self._sort_deps()
    
    def _init(self):
        self._dep_m = {}
        self._entries = []
        self._entry_m = {}
        self._scope_s = []
        self._in_field_s = []

    def _sort_deps(self):
        result = list(toposort.toposort(self._dep_m))

        ret = []
        for entries in result:
            for ei in entries:
                ret.append(self._entries[ei])
        return ret


    def visitDataTypeStruct(self, i: DataTypeStruct):
        is_new = False
        self.push_scope(i)
        if self.in_field():
            is_new = self.addRef(i)
        else:
            is_new = self.addType(i)

        for f in i.getFields():
            f.accept(self)

        self.pop_scope()

    def visitTypeField(self, i: TypeField):
        self.push_in_field(True)
        i.getDataType().accept(self)
        self.pop_in_field()

    def addType(self, i):
        is_new = True if i.name() not in self._entry_m.keys() else False
        if is_new:
            i_id = len(self._entries)
            self._entry_m[i.name()] = i_id
            self._dep_m[i_id] = []
            self._entries.append(i)
        else:
            i_id = self._entry_m[i.name()]
        return is_new
    
    def addRef(self, i):
        is_new = False
        if i.name() not in self._entry_m.keys():
            is_new = self.addType(i)

        dep_id = self._entry_m[self._scope_s[-1].name()]
        i_id = self._entry_m[i.name()]
        if i_id not in self._dep_m[dep_id]:
            self._dep_m[dep_id].append(i_id)
        return is_new

    def push_scope(self, s):
        self._scope_s.append(s)

    def scope(self):
        return self._scope_s[-1] if len(self._scope_s) > 0 else None
    
    def pop_scope(self):
        self._scope_s.pop()

    def push_in_field(self, i):
        self._in_field_s.append(i)
    
    def in_field(self):
        return len(self._in_field_s) and self._in_field_s[-1]
    
    def pop_in_field(self):
        self._in_field_s.pop()


