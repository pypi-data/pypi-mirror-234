#****************************************************************************
#* visitor_base.py
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

from .data_type_list import DataTypeList
from .data_type_list_fixed_size import DataTypeListFixedSize
from .data_type_int import DataTypeInt
from .data_type_struct import DataTypeStruct
from .type_constraint import TypeConstraint
from .type_constraint_block import TypeConstraintBlock
from .type_constraint_expr import TypeConstraintExpr
from .type_expr_bin import TypeExprBin
from .type_expr_field_ref import TypeExprFieldRef
from .type_expr_val import TypeExprVal
from .type_field import TypeField
from .type_field_phy import TypeFieldPhy
from .type_field_ref import TypeFieldRef

class VisitorBase(object):

    def visitDataTypeInt(self, i : DataTypeInt):
        pass

    def visitDataTypeList(self, i : DataTypeList):
        i.getElemType().accept(self)

    def visitDataTypeListFixedSize(self, i : DataTypeListFixedSize):
        self.visitDataTypeList(i)

    def visitDataTypeStruct(self, i : DataTypeStruct):
        for f in i.getFields():
            f.accept(self)
        for c in i.getConstraints():
            c.accept(self)

    def visitTypeConstraint(self, i : TypeConstraint):
        pass

    def visitTypeConstraintBlock(self, i : TypeConstraintBlock):
        for c in i.getConstraints():
            c.accept(self)

    def visitTypeConstraintExpr(self, i : TypeConstraintExpr):
        i.expr().accept(self)

    def visitTypeExprBin(self, i : TypeExprBin):
        i._lhs.accept(self)
        i._rhs.accept(self)

    def visitTypeExprFieldRef(self, i : TypeExprFieldRef):
        pass

    def visitTypeExprVal(self, i : TypeExprVal):
        pass

    def visitTypeField(self, i : TypeField):
        i.getDataType().accept(self)

    def visitTypeFieldPhy(self, i : TypeFieldPhy):
        self.visitTypeField(i)

    def visitTypeFieldRef(self, i : TypeFieldRef):
        self.visitTypeField(i)

