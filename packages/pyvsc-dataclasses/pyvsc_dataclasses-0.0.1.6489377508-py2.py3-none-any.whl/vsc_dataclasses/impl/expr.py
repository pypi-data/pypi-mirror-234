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
# Created on Mar 20, 2022
#
# @author: mballance
#****************************************************************************
from .ctor import Ctor
from .context import BinOp, UnaryOp

class Expr(object):
    
    def __init__(self, model):
        self._model = model
        Ctor.inst().push_expr(self)

    @property
    def model(self):
        return self._model
        
    @staticmethod
    def toExpr(rhs):
        if isinstance(rhs, Expr):
            return rhs
        elif hasattr(rhs, "_to_expr"):
            return rhs._to_expr()
        elif type(rhs) == int:
            ctor = Ctor.inst()
           
            ev = Ctor.inst().ctxt().mkTypeExprVal(
                Ctor.inst().ctxt().mkValRefInt(rhs, True, 64))
            return Expr(ev)
        else:
            raise Exception("toExpr failed: rhs=%s" % str(rhs))

    def _bin_expr(self, op, rhs):
        ctor = Ctor.inst()
        ctxt = ctor.ctxt()
        
        rhs_e = Expr.toExpr(rhs)
        lhs_e = self._model

        ctor.pop_expr(rhs)
        ctor.pop_expr()
       
        model = ctxt.mkModelExprBin(
            lhs_e, 
            op, 
            rhs_e)
        
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
    
    # TODO: is this needed?    
    def __call__(self, T):
        return T    
    
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
        return self._bin_expr(BinOp.And, rhs)
    
    def __or__(self, rhs):
        return self._bin_expr(BinOp.Or, rhs)
    
    def __xor__(self, rhs):
        return self._bin_expr(BinOp.Xor, rhs)
    
    def __lshift__(self, rhs):
        return self._bin_expr(BinOp.Sll, rhs)
    
    def __rshift__(self, rhs):
        return self._bin_expr(BinOp.Srl, rhs)
    
    def __neg__(self):
        return self._bin_expr(BinOp.Not, rhs)    
    
    def __invert__(self):
        lhs = pop_expr()
        
        return expr(ExprUnaryModel(UnaryExprType.Not, lhs))
    
    def inside(self, rhs):
        lhs_e = pop_expr()
        
        if isinstance(rhs, rangelist):
            return expr(ExprInModel(lhs_e, rhs.range_l))
        elif isinstance(rhs, list_t):
            return expr(ExprInModel(
                lhs_e,
                ExprRangelistModel(
                    [ExprFieldRefModel(rhs.get_model())])))
        else:
            raise Exception("Unsupported 'inside' argument of type " + str(type(rhs)) + 
                            "expect vsc.rangelist or list_t")

    def outside(self, rhs):
        self.not_inside(rhs)
            
    def not_inside(self, rhs):
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
            raise Exception("Unsupported 'not_inside' argument of type " + str(type(rhs)))
        
    def __getitem__(self, k):
        if is_expr_mode():
            if isinstance(k, slice):
                # Part-select on a field expression
                print("k=" + str(k) + " start=" + str(k.start) + " stop=" + str(k.stop))
                
                to_expr(k.start)
                upper = pop_expr()
                to_expr(k.stop)
                lower = pop_expr()
                
                base_e = pop_expr()
                return expr(ExprPartselectModel(base_e, upper, lower))
            else:
                # single value
                to_expr(k)
                idx_e = pop_expr()
                base_e = pop_expr()
                
                return expr_subscript(ExprArraySubscriptModel(
                    base_e,
                    idx_e))
        else:
            raise Exception("Calling __getitem__ on an expr on non-expression context")    