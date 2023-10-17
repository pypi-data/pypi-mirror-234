#****************************************************************************
#* vsc_data_model_cpp_gen.py
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

from ..pyctxt.type_expr_val import TypeExprVal
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
from ..pyctxt.visitor_base import VisitorBase

class VscDataModelCppGen(VisitorBase):

    def __init__(self, ind=""):
        self._ind = ind
        self._out = io.StringIO()
        self._type_s = []
        self._constraint_scope_s = []
        self._ctxt = "ctxt"
        # When >0, we're referencing the type not defining it
        self._emit_type_mode = 0
        self._comma = []

    def generate(self, cls : DataTypeStruct):
        self._out = io.StringIO()
        cls_l = CollectStructDeps(None).collect(cls)

        for i,cls_t in enumerate(cls_l):
#            self._field_ctor.clear()

            if i > 0:
                self._out.write("\n")
            cls_t.accept(self)

        return self._out.getvalue()

    def visitDataTypeInt(self, i: DataTypeInt):
        if self._emit_type_mode > 0:
            # We're locating the desired type
            self.write("%s->findDataTypeInt(%s, %d)" % (
                self._ctxt,
                "true" if i._is_signed else "false",
                i._width
            ))
        else:
            # We're declaring the type
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

    def visitTypeConstraintBlock(self, i: TypeConstraintBlock):
        t = self._type_s[-1]

        self._constraint_scope_s.append("%s_%s_c" % (self.leaf_name(t.name()), i.name()))

        self.println("vsc::dm::ITypeConstraintBlock *%s_%s_c = %s->mkTypeConstraintBlock(\"%s\");" % (
            self.leaf_name(t.name()), i.name(),
            self._ctxt, i.name()
        ))

        super().visitTypeConstraintBlock(i)
        self.println("%s_t->addConstraint(%s_%s_c);" % (
            self.leaf_name(t.name()), self.leaf_name(t.name()), i.name()))
        self._constraint_scope_s.pop()

    def visitTypeConstraintExpr(self, i: TypeConstraintExpr):
        self.println("%s->addConstraint(" % self._constraint_scope_s[-1])
        self.inc_indent()
        self.println("%s->mkTypeConstraintExpr(" % self._ctxt)
        self.inc_indent()
        i.expr().accept(self)
        self.dec_indent()
        self.println(")")
        self.dec_indent()
        self.println(");")

    def visitTypeExprBin(self, i: TypeExprBin):
        op_m = {
            BinOp.Eq : "vsc::dm::BinOp::Eq",
            BinOp.Ne : "vsc::dm::BinOp::Ne",
            BinOp.Gt : "vsc::dm::BinOp::Gt",
            BinOp.Ge : "vsc::dm::BinOp::Ge",
            BinOp.Lt : "vsc::dm::BinOp::Lt",
            BinOp.Le : "vsc::dm::BinOp::Le",
            BinOp.Add : "vsc::dm::BinOp::Add",
            BinOp.Sub : "vsc::dm::BinOp::Sub",
            BinOp.Div : "vsc::dm::BinOp::Div",
            BinOp.Mul : "vsc::dm::BinOp::Mul",
            BinOp.Mod : "vsc::dm::BinOp::Mod",
            BinOp.BinAnd : "vsc::dm::BinOp::BinAnd",
            BinOp.BinOr  : "vsc::dm::BinOp::BinOr",
            BinOp.LogAnd : "vsc::dm::BinOp::LogAnd",
            BinOp.LogOr  : "vsc::dm::BinOp::LogOr",
            BinOp.Sll    : "vsc::dm::BinOp::Sll",
            BinOp.Srl    : "vsc::dm::BinOp::Srl",
            BinOp.Xor    : "vsc::dm::BinOp::Xor",
            BinOp.Not    : "~"
        }
        self.println("%s->mkTypeExprBin(" % self._ctxt)
        self.inc_indent()
        self._comma.append(True)
        i._lhs.accept(self)
        self.println("%s," % op_m[i._op])
        self._comma.pop()
        self._comma.append(False)
        i._rhs.accept(self)
        self._comma.pop()
        self.dec_indent()
        self.println(")%s" % self.comma())

    def visitTypeExprFieldRef(self, i: TypeExprFieldRef):
        if i.getRootRefKind() == TypeExprFieldRefKind.TopDownScope:
            ref_base = "vsc::dm::ITypeExprFieldRef::RootRefKind::TopDownScope"
        else:
            ref_base = "vsc::dm::ITypeExprFieldRef::RootRefKind::BottomUpScope"

        ref_list_s = list(map(lambda i: str(i), i.getPath()))
        self.println("%s->mkTypeExprFieldRef(%s, %d, {%s})%s" % (
            self._ctxt,
            ref_base,
            i.getRootRefOffset(),
            ",".join(ref_list_s),
            self.comma()))

        # TODO: assume in type context
#        t = self._type_s[-1]
#
#        for ii in i.getPath():
#            f = t.getField(ii)
#            self.write("%s" % f.name())
#        return super().visitTypeExprFieldRef(i)

    def visitTypeExprVal(self, i: TypeExprVal):
        self.println("%s->mkTypeExprVal(" % self._ctxt)
        self.inc_indent()
        self.println("%s->mkValRefInt(%d, true, 32)" % (self._ctxt, i._val._val))
        self.dec_indent()
        self.println(")%s" % self.comma())
    
    def visitTypeFieldPhy(self, i: TypeFieldPhy):
        # First, find the type
        self.write("%svsc::dm::IDataType *%s_t = " % (self._ind, i.name()))
        self._emit_type_mode += 1
        i.getDataType().accept(self)
        self._emit_type_mode -= 1
        self.write(";\n")
        self.println("vsc::dm::ITypeField *%s = %s->mkTypeFieldPhy(\"%s\"," % (
            i.name(),
            self._ctxt,
            i.name()
        ))
        self.inc_indent()
        self.println("%s_t," % i.name())
        self.println("false,")
        flags = []
        for v in TypeFieldAttr:
            if int(v) & int(i._attr) != 0:
                flags.append(v)

        if len(flags) == 0:
            flags.append(TypeFieldAttr.NoAttr)

        self.println("%s," % "|".join(map(lambda i: "vsc::dm::TypeFieldAttr::%s" % str(i).split(".")[-1], flags)))
        self.println("vsc::dm::ValRef()")
        self.dec_indent()
        self.println(");")
        self.println("dynamic_cast<vsc::dm::IDataTypeStruct *>(%s_t)->addField(%s);" % (
            self.leaf_name(self._type_s[-1].name()),
            i.name()))

    def visitDataTypeStruct(self, i: DataTypeStruct):
        self._type_s.append(i)

        if self._emit_type_mode > 0:
            # We're emitting the type in order to declare a field
            self.write("%s->findDataTypeStruct(\"%s\")" % (self._ctxt, self.leaf_name(i.name())))
        else:
            # We're declaring a type
            self.println("vsc::dm::IDataTypeStruct *%s_t = %s->mkDataTypeStruct(\"%s\");" % (
                self.leaf_name(i.name()),
                self._ctxt,
                self.leaf_name(i.name())))
            self.println("{")
            self.inc_indent()
            super().visitDataTypeStruct(i)
            self.println("%s->addDataTypeStruct(%s_t);" % (
                self._ctxt,
                self.leaf_name(i.name())))
            self.dec_indent()
            self.println("}")

        self._type_s.pop()
    
    def println(self, data):
        self._out.write(self._ind)
        self._out.write(data)
        self._out.write("\n")

    def write(self, data):
        self._out.write(data)

    def inc_indent(self):
        self._ind += "    "

    def ind(self):
        return self._ind

    def dec_indent(self):
        if len(self._ind) > 4:
            self._ind = self._ind[:-4]
        else:
            self._ind = ""

    def push_comma(self, c=True):
        self._comma.append(c)

    def comma(self):
        return "," if len(self._comma) > 0 and self._comma[-1] else ""
    
    def pop_comma(self):
        self._comma.pop()

    def leaf_name(self, name):
        elems = name.split('.')
        return elems[-1]
    
    def localname(self, name):
        lidx = name.find("<locals>.")
        if lidx != -1:
            return name[lidx+9:]
        else:
            return name
