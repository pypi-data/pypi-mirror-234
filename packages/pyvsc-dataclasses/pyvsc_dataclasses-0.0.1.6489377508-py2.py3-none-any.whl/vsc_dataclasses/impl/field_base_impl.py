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
# Created on May 25, 2022
#
# @author: mballance
#****************************************************************************

import logging

from .context import Context
from .context import TypeExprFieldRefKind

from .ctor import Ctor
from .expr import Expr
from .modelinfo import ModelInfo


class FieldBaseImpl(object):
    
    def __init__(self, name, typeinfo, idx):
        self._modelinfo = ModelInfo(self, name, typeinfo, idx)
        self._logger = logging.getLogger(type(self).__name__)
        
    def _to_expr(self):
        ctor = Ctor.inst()

        if ctor.is_type_mode():
            self._logger.debug("FieldScalarImpl._to_expr (%s)" % self._modelinfo.name)
            mi = self._modelinfo
            self._logger.debug("is_topdown_scope: %d" % mi._is_topdown_scope)
            offset_l = []

            # Walk up the stack until we find the root
            last_parent = None
            while mi._parent is not None:
                last_parent = mi._parent
                self._logger.debug("  IDX: %d" % mi._idx)
                offset_l.insert(0, mi._idx)
                self._logger.debug("MI: %s" % str(mi))
                mi = mi._parent

            print("Last Parent: %s" % str(last_parent))

            bottom_up_offset = -1
            for ii,s in enumerate(ctor.bottom_up_scopes()[::-1]):
                if s is last_parent:
                    bottom_up_offset = ii
                    break
            
            print("bottom_up_offset: %d" % bottom_up_offset)
            offset = 0
            kind = TypeExprFieldRefKind.TopDownScope

            if bottom_up_offset != -1:
                offset = bottom_up_offset
                kind = TypeExprFieldRefKind.BottomUpScope

            ref = ctor.ctxt().mkTypeExprFieldRef(kind, offset, offset_l)
        else:        
            self._logger.debug("FieldScalarImpl._to_expr (%s)" % self.model().name())
            ref = ctor.ctxt().mkModelExprFieldRef(self.model())
        
        return Expr(ref)
    
