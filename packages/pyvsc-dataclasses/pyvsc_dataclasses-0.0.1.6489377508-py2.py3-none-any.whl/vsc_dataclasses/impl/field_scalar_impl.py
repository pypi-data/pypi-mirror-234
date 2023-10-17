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
# Created on Mar 11, 2022
#
# @author: mballance
#****************************************************************************
from .context import BinOp, UnaryOp

from .ctor import Ctor
from .expr import Expr
from .field_base_impl import FieldBaseImpl
from .modelinfo import ModelInfo
from .typeinfo_vsc import TypeInfoVsc
from .type_kind_e import TypeKindE


class FieldScalarImpl(FieldBaseImpl):
    
    def __init__(self, name, typeinfo, idx):
        ctor = Ctor.inst()
        super().__init__(name, typeinfo, idx)
        self._is_signed = typeinfo.is_signed

    def get_val(self, modelinfo_p):
        ctor = Ctor.inst()
        if not ctor.is_type_mode():
            field = modelinfo_p.libobj.getField(self._modelinfo.idx)
            if self._is_signed:
                return field.val().val_i()
            else:
                return field.val().val_u()
        else:
            return 0
    
    def set_val(self, modelinfo_p, v):
        ctor = Ctor.inst()
        if not ctor.is_type_mode():
            field = modelinfo_p.libobj.getField(self._modelinfo.idx)
            if self._is_signed:
                field.val().set_val_i(v)
            else:
                field.val().set_val_u(v)

    @property        
    def val(self):
        return self._modelinfo._lib_obj.val().val_i()

    @val.setter
    def val(self, v):
        self._modelinfo._lib_obj.val().set_val_i(v)
        

    
    def _bin_expr(self, op, rhs):
        ctor = Ctor.inst()
        
        self._logger.debug("_bin_expr: op=%s" % op)

        if isinstance(rhs, Expr):
            rhs_e = rhs
        else:
            rhs_e = Expr.toExpr(rhs)
            
        ctor.pop_expr(rhs_e)

#        push_expr(ExprFieldRefModel(self._int_field_info.model))
        # Push a reference to this field
        lhs_e = Expr.toExpr(self)
        ctor.pop_expr(lhs_e)
        
        self._logger.debug("lhs_e=%s rhs_e=%s" % (str(lhs_e), str(rhs_e)))

        if ctor.is_type_mode():
            model = ctor.ctxt().mkTypeExprBin(
                lhs_e._model, 
                op, 
                rhs_e._model)
        else:        
            model = ctor.ctxt().mkModelExprBin(
                lhs_e._model, 
                op, 
                rhs_e._model)
            
#        if in_srcinfo_mode():
#            e.srcinfo = SourceInfo.mk(2)
        
        return Expr(model)

    def __eq__(self, rhs):
        return self._bin_expr(BinOp.Eq, rhs)
    
    def __ne__(self, rhs):
        return self._bin_expr(BinOp.Ne, rhs)
    
    def __le__(self, rhs):
        return self._bin_expr(BinOp.Le, rhs)
    
    def __lt__(self, rhs):
        return self._bin_expr(BinOp.Lt, rhs)
    
    def __ge__(self, rhs):
        return self._bin_expr(BinOp.Ge, rhs)
    
    def __gt__(self, rhs):
        return self._bin_expr(BinOp.Gt, rhs)
    
    def __add__(self, rhs):
        return self._bin_expr(BinOp.Add, rhs)
    
    def __sub__(self, rhs):
        return self._bin_expr(BinOp.Sub, rhs)
    
    def __truediv__(self, rhs):
        return self._bin_expr(BinOp.Div, rhs)
    
    def __floordiv__(self, rhs):
        return self._bin_expr(BinOp.Div, rhs)
    
    def __mul__(self, rhs):
        return self._bin_expr(BinOp.Mul, rhs)
    
    def __mod__(self, rhs):
        return self._bin_expr(BinOp.Mod, rhs)
    
    def __and__(self, rhs):
        return self._bin_expr(BinOp.BinAnd, rhs)
    
    def __or__(self, rhs):
        return self._bin_expr(BinOp.BinOr, rhs)
    
    def __xor__(self, rhs):
        return self._bin_expr(BinOp.Xor, rhs)
    
    def __lshift__(self, rhs):
        return self._bin_expr(BinOp.Sll, rhs)
    
    def __rshift__(self, rhs):
        return self._bin_expr(BinOp.Srl, rhs)
    
    def __neg__(self):
        return self._bin_expr(BinOp.Not, rhs)
   
    def __invert__(self): 
        ctor = Ctor.inst()
        lhs = Expr.toExpr(self)
        ctor.pop_expr(lhs)

        if ctor.is_type_mode():
            raise Exception("mkTypeExprUnary not supported")
        else:
            return Expr(ctor.ctxt().mkExprModelUnary(UnaryOp.Not, lhs))
    
    def inside(self, rhs):
        self.to_expr()
        lhs_e = pop_expr()
        
        if isinstance(rhs, rangelist):
            return expr(ExprInModel(lhs_e, rhs.range_l))
        elif isinstance(rhs, rng):
            rl = ExprRangelistModel()
            rl.add_range(ExprRangeModel(rhs.low, rhs.high))
            return expr(ExprInModel(lhs_e, rl))
        elif isinstance(rhs, list_t):
            return expr(ExprInModel(
                lhs_e,
                ExprRangelistModel(
                    [ExprFieldRefModel(rhs.get_model())])))
        else:
            raise Exception("Unsupported 'inside' argument of type " + str(type(rhs)))

    def outside(self, rhs):
        self.not_inside(rhs)
            
    def not_inside(self, rhs):
        self.to_expr()
        lhs_e = pop_expr()
        
        if isinstance(rhs, rangelist):
            return expr(ExprUnaryModel(
                UnaryExprType.Not,
                ExprInModel(lhs_e, rhs.range_l)))
        elif isinstance(rhs, list_t):
            return expr(ExprUnaryModel(
                UnaryExprType.Not,
                ExprInModel(lhs_e,
                    ExprRangelistModel(
                        [ExprFieldRefModel(rhs.get_model())]))))
        else:
            raise Exception("Unsupported 'not_inside' argument of type " + str(type(rhs)) + " expect rangelist or list_t")
        
    
        
    def __getitem__(self, rng):
        ctor = Ctor.inst()
        
        if ctor.expr_mode():
            if isinstance(rng, slice):
                # slice
                upper = Expr.toExpr(rng.start)
                upper = ctor.pop_expr(upper)
                Expr.toExpr(rng.stop)
                lower = ctor.pop_expr()
                if ctor.is_type_mode():
                    raise Exception("mkTypeExprPartSelect not implemented")
                else:
                    return Expr(ctor.ctxt().mkModelExprPartSelect(
                        ctor.ctxt().mkModelExprFieldRefModel(self._modelinfo._lib_obj), 
                        upper, 
                        lower))
            else:
                # single value
                Expr.toExpr(rng)
                e = ctor.pop_expr()
                if ctor.is_type_mode():
                    raise Exception("mkTypeExprPartSelect not implemented")
                else:
                    return Expr(ctor.ctxt().mkModelExprPartSelect(
                        ctor.ctxt().mkModelExprFieldRef(self._modelinfo._lib_obj), e, e))
        else:
            curr = int(self.get_model().get_val())
            if isinstance(rng, slice):
                msk = ((1 << (rng.start-rng.stop+1))-1) << rng.stop
                curr = (curr & msk) >> rng.stop
            else:
                curr = (curr & (1 << rng)) >> rng
            return curr
            
    def __setitem__(self, rng, val):
        ctor = Ctor.inst()
        if not ctor.expr_mode():
            curr = int(self.get_model().get_val())
            if isinstance(rng, slice):
                msk = ((1 << (rng.start-rng.stop))-1) << rng.stop
                curr = (curr & msk) | (val << rng.stop & msk)
            else:
                curr = (curr & ~(val << rng)) | (val << rng)
            self.get_model().set_val(curr)
        else:
            raise Exception("Cannot assign to a part-select within a constraint")    


    
