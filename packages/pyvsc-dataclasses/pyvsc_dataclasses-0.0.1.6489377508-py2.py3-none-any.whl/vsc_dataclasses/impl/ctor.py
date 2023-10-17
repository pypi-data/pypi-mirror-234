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
#from libvsc import core
from .ctor_scope import CtorScope

class Ctor():
    
    _inst = None
    
    def __init__(self):

        self._ctxt = None
        
        self._scope_s = []
        self._typemode_s = []
        self._constraint_l = []
        self._constraint_s = []
        self._expr_s = []
        self._expr_mode_s = []
        self._raw_mode_s = []
        self._bottom_up_scopes_s = []
        self._type_ps = "."
    
    def ctxt(self):
        return self._ctxt

    def setTypePS(self, ps):
        ret = self._type_ps
        self._type_ps = ps
        return ret

    def pyType2TypeName(self, name):
        """Creates a type name from a Python-type name"""
        if self._type_ps != ".":
            return name.replace('.', self._type_ps)
        else:
            return name

    def mkRandState(self):
        from .rand_state import RandState

        return RandState(f"{self._randstate.rand_u}")

    def save_scopes(self, clear=True):
        ret = self._scope_s.copy()
        if clear:
            self._scope_s.clear()
        return ret

    def restore_scopes(self, scopes):
        self._scope_s = scopes
    
    def scope(self, off=-1):
        if len(self._scope_s) > 0:
            return self._scope_s[off]
        else:
            return None
        
    def push_scope(self, facade_obj, lib_scope, type_mode):
        s = CtorScope(facade_obj, lib_scope, type_mode)
        self._scope_s.append(s)
        return s
        
    def pop_scope(self):
        self._scope_s.pop()

    def push_type_mode(self, t=True):
        self._typemode_s.append(t)

    def is_type_mode(self):
        return (len(self._typemode_s) > 0 and self._typemode_s[-1]) or len(self._scope_s) > 0 and self._scope_s[-1]._type_mode

    def pop_type_mode(self):
        self._typemode_s.pop()

    def push_bottom_up_scope(self, si):
        self._bottom_up_scopes_s.append(si)

    def bottom_up_scopes(self):
        return self._bottom_up_scopes_s

    def bottom_up_scope(self):
        return self._bottom_up_scopes_s[-1]
    
    def pop_bottom_up_scope(self):
        return self._bottom_up_scopes_s.pop()
        
    def push_expr(self, e):
        self._expr_s.append(e)
        
    def pop_expr(self, e=None):
        if e is not None:
            if self._expr_s[-1] is e:
                return self._expr_s.pop()
            elif len(self._expr_s) > 1 and self._expr_s[-2] is e:
                return self.expr_e.pop(-2)
            else:
                raise Exception("Failed to find target")
        else:
            return self._expr_s.pop()
        
    def pop_exprs(self):
        ret = self._expr_s.copy()
        self._expr_s.clear()
        return ret
        
    def expr(self):
        if len(self._expr_s) > 0:
            return self._expr_s[-1]
        else:
            return None
        
    def push_expr_mode(self, m=True):
        self._expr_mode_s.append(m)
        
    def expr_mode(self):
        return len(self._expr_mode_s) > 0 and self._expr_mode_s[-1]
        
    def pop_expr_mode(self):
        return self._expr_mode_s.pop()

    def push_raw_mode(self, m=True):
        self._raw_mode_s.append(m)

    def raw_mode(self):
        return len(self._raw_mode_s) and self._raw_mode_s[-1]

    def pop_raw_mode(self):
        return self._raw_mode_s.pop()
        
    def push_constraint_decl(self, c):
        self._constraint_l.append(c)
        
    def pop_constraint_decl(self):
        ret = self._constraint_l.copy()
        self._constraint_l.clear()
        return ret
    
    def push_constraint_scope(self, c):
        self._constraint_s.append(c)

    def in_constraint_scope(self):
        return len(self._constraint_s) > 0

    def constraint_scope(self):
        return self._constraint_s[-1]

    def last_constraint_stmt(self):
        if len(self._constraint_s) > 0:
            return self._constraint_s[-1].constraints()[-1]
        else:
            return None
    
    def pop_constraint_scope(self):
        # Collect remaining expressions and convert to expr_statements
        cb = self._constraint_s.pop()
        
        for e in self._expr_s:
            if self.is_type_mode():
                c = self.ctxt().mkTypeConstraintExpr(e._model)
            else:
                c = self.ctxt().mkModelConstraintExpr(e._model)
            cb.addConstraint(c)
        self._expr_s.clear()
            
        return cb
    
    @classmethod
    def inst(cls):
        if cls._inst is None:
            from .rand_state import RandState
            cls._inst = Ctor()
            cls._inst._randstate = RandState.mk()
        return cls._inst

    @classmethod
    def init(cls, ctxt):
        cls._inst = Ctor()
        cls._inst._ctxt = ctxt
        cls._inst._randstate = None
        