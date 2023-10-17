#****************************************************************************
#* system_verilog_class_gen.py
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
from vsc_dataclasses.impl.pyctxt.data_type_list import DataTypeList
from vsc_dataclasses.impl.pyctxt.data_type_list_fixed_size import DataTypeListFixedSize
from vsc_dataclasses.impl.pyctxt.data_type_struct import DataTypeStruct
from vsc_dataclasses.impl.pyctxt.type_constraint_block import TypeConstraintBlock
from vsc_dataclasses.impl.pyctxt.type_constraint_expr import TypeConstraintExpr
from vsc_dataclasses.impl.pyctxt.type_expr_bin import TypeExprBin
from vsc_dataclasses.impl.pyctxt.type_expr_field_ref import TypeExprFieldRef
from vsc_dataclasses.impl.pyctxt.type_field_phy import TypeFieldPhy
from ..context import BinOp
from ..pyctxt.data_type_struct import DataTypeStruct
from ..pyctxt.type_expr_val import TypeExprVal
from ..pyctxt.visitor_base import VisitorBase
from .collect_struct_deps import CollectStructDeps

class SystemVerilogClassGen(VisitorBase):

    def __init__(self):
        self._ind = ""
        self._out = io.StringIO()
        self._type_s = []
        self._field_name_s = []
        self._field_ctor = []
        self._emit_type_mode = 0
        pass

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
        self.println("function new();")
        self.inc_indent()
        for c in self._field_ctor:
            c()
        self.dec_indent()
        self.println("endfunction")
        pass
    
    def visitDataTypeInt(self, i: DataTypeInt):
        if self._emit_type_mode == 0:
            return

        if (i._is_signed):
            if i._width == 1:
                self.write("bit signed")
            else:
                self.write("bit[%d:0] signed" % (i._width-1))
        else:
            if i._width == 1:
                self.write("bit")
            else:
                self.write("bit[%d:0]" % (i._width-1))

    def visitDataTypeList(self, i: DataTypeList):
        raise Exception("Variable-size arrays are not supported")
    
    def visitDataTypeListFixedSize(self, i: DataTypeListFixedSize):
        # Processing is bottom-up
        i.getElemType().accept(self)

        if self._emit_type_mode == 0:
            self.write("[%0d]" % i.getSize())

    def visitTypeConstraintBlock(self, i: TypeConstraintBlock):
        self.println("constraint %s {" % i.name())
        self.inc_indent()
        super().visitTypeConstraintBlock(i)
        self.dec_indent()
        self.println("}")

    def visitTypeConstraintExpr(self, i: TypeConstraintExpr):
        self.write(self._ind)
        super().visitTypeConstraintExpr(i)
        self.write(";\n")

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
        self.write(" %s " % op_m[i._op])
        i._rhs.accept(self)

    def visitTypeExprFieldRef(self, i: TypeExprFieldRef):
        # TODO: assume in type context
        t = self._type_s[-1]

        for iii,ii in enumerate(i.getPath()):
            if iii > 0:
                self.write(".")
            f = t.getField(ii)
            self.write("%s" % f.name())

        return super().visitTypeExprFieldRef(i)

    def visitTypeExprVal(self, i: TypeExprVal):
        self.write("%d" % i._val._val)
    
    def visitTypeFieldPhy(self, i: TypeFieldPhy):
        self._field_name_s.append(i.name())
        self.write("%srand " % self._ind)
        self._emit_type_mode += 1
        i.getDataType().accept(self)
        self._emit_type_mode -= 1
        self.write(" %s" % i.name())

        # Emit the size dimensions
        if isinstance(i.getDataType(), DataTypeListFixedSize):
            i.getDataType().accept(self)

        self.write(";\n")
        self._field_name_s.pop()
    
    def visitDataTypeStruct(self, i: DataTypeStruct):
        if len(self._type_s) > 0:
            if self._emit_type_mode != 0:
                # This is a field, so just display the typename
                self.write("%s" % self.leaf_name(i.name()))

                if len(self._field_name_s) > 0:
                    def write_ctor(name):
                        self.println("%s = new();" % name)
                    name = self._field_name_s[-1]
                    self._field_ctor.append(lambda : write_ctor(name))
        else:
            # Render the type declaration
            self._type_s.append(i)

            self.println("class %s;" % self.leaf_name(i.name()))
            self.inc_indent()
            super().visitDataTypeStruct(i)

            if len(self._type_s) == 1:
                self.println()
                self._build_ctor()
                self.println()

            self.dec_indent()
            self.println("endclass")
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

