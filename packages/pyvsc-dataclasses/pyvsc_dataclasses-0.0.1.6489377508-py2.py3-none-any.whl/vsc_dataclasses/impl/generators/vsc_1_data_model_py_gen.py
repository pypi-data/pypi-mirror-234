#****************************************************************************
#* vsc_1_data_model_py_gen.py
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
from vsc_dataclasses.impl.pyctxt.data_type_int import DataTypeInt
from vsc_dataclasses.impl.pyctxt.data_type_struct import DataTypeStruct
from vsc_dataclasses.impl.pyctxt.type_constraint_block import TypeConstraintBlock
from vsc_dataclasses.impl.pyctxt.type_constraint_expr import TypeConstraintExpr
from vsc_dataclasses.impl.pyctxt.type_expr_bin import TypeExprBin
from vsc_dataclasses.impl.pyctxt.type_expr_field_ref import TypeExprFieldRef
from vsc_dataclasses.impl.pyctxt.type_field_phy import TypeFieldPhy
from .collect_struct_deps import CollectStructDeps
from ..context import BinOp, TypeExprFieldRefKind, TypeFieldAttr
from ..pyctxt.data_type_struct import DataTypeStruct
from ..pyctxt.type_expr_val import TypeExprVal
from ..pyctxt.visitor_base import VisitorBase

class Vsc1DataModelPyGen(VisitorBase):

    def __init__(self):
        self._ind = ""
        self._out = io.StringIO()
        self._type_s = []
        self._field_name_s = []
        self._field_ctor = []
        self._emit_type_mode = 0
        self._type_is_rand = False
#        self._type_ctor = ""
        self._content = ""


    def generate(self, cls : DataTypeStruct):
        self._out = io.StringIO()

        cls_l = CollectStructDeps(None).collect(cls)

        for i,cls_t in enumerate(cls_l):
            self._field_ctor.clear()

            if i > 0:
                self._out.write("\n")
            cls_t.accept(self)

        return self._out.getvalue()
    
    def _build_ctor(self):
        self.println("def __init__(self):")
        self.inc_indent()
        for c in self._field_ctor:
            self.println(c)
        if len(self._field_ctor) == 0:
            self.println("pass")
        self.dec_indent()
    
    def visitDataTypeInt(self, i: DataTypeInt):
        if self._emit_type_mode == 0:
            return

        self._content += "vsc.%s%s(%d)" % (
            "rand_" if self._type_is_rand else "",
            "int_t" if i._is_signed else "bit_t",
            i._width)

    def visitDataTypeList(self, i: 'DataTypeList'):
        raise Exception("Variable-size arrays are not supported")
    
    def visitDataTypeListFixedSize(self, i: 'DataTypeListFixedSize'):
        # Processing is bottom-up

        self._content += "vsc.%slist_t(" % "rand_" if self._type_is_rand else ""
        i.getElemType().accept(self)
        self._content += ", %d)" % i.getSize()

#        if self._emit_type_mode == 0:
#            self.write("[%0d]" % i.getSize())

    def visitTypeConstraintBlock(self, i: TypeConstraintBlock):
        self.println("@vsc.constraint")
        self.println("def %s(self):" % i.name())
        self.inc_indent()
        super().visitTypeConstraintBlock(i)
        self.dec_indent()
        self.println()

    def visitTypeConstraintExpr(self, i: TypeConstraintExpr):
        self.write(self._ind)
        self._content = ""
        super().visitTypeConstraintExpr(i)
        self.write("%s\n" % self._content)
        self._content = ""

    def visitTypeExprBin(self, i: TypeExprBin):
        op_m = {
            BinOp.Eq : "==",
            BinOp.Ne : "!=",
            BinOp.Gt : ">",
            BinOp.Ge : ">=",
            BinOp.Lt : "<",
            BinOp.Le : "<=",
            BinOp.Add : "+",
            BinOp.Sub : "-",
            BinOp.Div : "/",
            BinOp.Mul : "*",
            BinOp.Mod : "%",
            BinOp.BinAnd : "&",
            BinOp.BinOr  : "|",
            BinOp.LogAnd : "&&",
            BinOp.LogOr  : "||",
            BinOp.Sll    : "<<",
            BinOp.Srl    : ">>",
            BinOp.Xor    : "^",
            BinOp.Not    : "~"
        }

        i._lhs.accept(self)
        self._content += " %s " % op_m[i._op]
        i._rhs.accept(self)

    def visitTypeExprFieldRef(self, i: TypeExprFieldRef):
        # TODO: assume in type context
        t = self._type_s[-1]

        self._content += "self"
        for ii in i.getPath():
            self._content += "."
            f = t.getField(ii)
            self._content += "%s" % f.name()

        return super().visitTypeExprFieldRef(i)

    def visitTypeExprVal(self, i: TypeExprVal):
        self.write("%d" % i._val._val)
    
    def visitTypeFieldPhy(self, i: TypeFieldPhy):
        self._type_is_rand = True
        self._content = ""


        self._field_name_s.append(i.name())
        self._emit_type_mode += 1
        i.getDataType().accept(self)
        self._emit_type_mode -= 1
        
        self._field_ctor.append("self.%s = %s" % (
            i.name(),
            self._content))

        # Emit the size dimensions
#        if isinstance(i.getDataType(), DataTypeListFixedSize):
#            i.getDataType().accept(self)

        self._field_name_s.pop()
    
    def visitDataTypeStruct(self, i: DataTypeStruct):
        if len(self._type_s) > 0:
            # We're inside a type declaration, so just render 
            # the type name
            if self._emit_type_mode != 0:
                self._content = "vsc.%sattr(%s())" % (
                    "rand_" if self._type_is_rand else "",
                    self.leaf_name(i.name()))
        else:
            # Render the type declaration
            self._type_s.append(i)

            self.println("@vsc.randobj")
            self.println("class %s(object):" % self.leaf_name(i.name()))
            self.inc_indent()
            super().visitDataTypeStruct(i)

            if len(self._type_s) == 1:
                self.println()
                self._build_ctor()
                self.println()

            self.dec_indent()
            self._type_s.pop()
    
    def println(self, data=""):
        self._out.write(self._ind)
        self._out.write(data)
        self._out.write("\n")

    def write(self, data):
        self._out.write(data)

    def inc_indent(self):
        self._ind += "    "

    def dec_indent(self):
        if len(self._ind) > 4:
            self._ind = self._ind[:-4]
        else:
            self._ind = ""

    def leaf_name(self, name):
        elems = name.split('.')
        return elems[-1]
