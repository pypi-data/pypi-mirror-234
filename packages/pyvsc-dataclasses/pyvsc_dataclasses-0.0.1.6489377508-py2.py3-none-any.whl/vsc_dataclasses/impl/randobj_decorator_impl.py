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
# Created on May 22, 2022
#
# @author: mballance
#****************************************************************************
from .ctor import Ctor
from .typeinfo_randclass import TypeInfoRandClass
from .randobj_impl import RandObjImpl
from .type_kind_e import TypeKindE


class RandObjDecoratorImpl(object):
    
    def __init__(self, kwargs):
        pass
    
    def __call__(self, T):
        ctor = Ctor.inst()
        
        T._typeinfo = TypeInfoRandClass(None, TypeKindE.RandObj)
        
        RandObjImpl.addMethods(T)
        
        constraints = Ctor.inst().pop_constraint_decl()
        T._typeinfo._constraint_l.extend(constraints)
        
        for c in constraints:
            T._typeinfo._constraint_m[c._name] = c
            
        for b in T.__bases__:
            if hasattr(b, "_typeinfo"):
                self.__collectConstraints(T._typeinfo, b)
                
        print("Constraints: %s" % str(T._typeinfo._constraint_l))
        
        return T
    
    def __collectConstraints(self, typeinfo, clsT):
        """Connect constraints from base classes"""
        # First, connect any additional constraints registered in the base class
        for cn,cd in clsT._typeinfo._constraint_m.items():
            if cn not in typeinfo._constraint_m.keys():
                print("Adding base-class %s" % cn)
                typeinfo._constraint_l.append(cd)
                typeinfo._constraint_m[cn] = cd
            else:
                print("Skipping overridden %s" % cn)
                pass
                
        # Now, keep digging
        for b in clsT.__bases__:
            if hasattr(b, "_typeinfo"):
                self.__collectConstraints(typeinfo, b)

