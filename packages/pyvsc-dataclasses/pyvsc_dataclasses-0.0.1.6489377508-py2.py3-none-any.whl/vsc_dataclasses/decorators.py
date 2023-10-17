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
# Created on Feb 26, 2022
#
# @author: mballance
#****************************************************************************

from .impl.constraint_decorator_impl import ConstraintDecoratorImpl
from .impl.extend_randclass_decorator_impl import ExtendRandClassDecoratorImpl
from .impl.randobj_decorator_impl import RandObjDecoratorImpl
from .impl.randclass_decorator_impl import RandClassDecoratorImpl
from .impl.covergroup_decorator_impl import CovergroupDecoratorImpl


def constraint(*args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # No-argument form
        return ConstraintDecoratorImpl({})(args[0])
    else:
        return ConstraintDecoratorImpl(kwargs)
    
def covergroup(*args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # No-argument form
        return CovergroupDecoratorImpl({})(args[0])
    else:
        return CovergroupDecoratorImpl(kwargs)

def extend(target, *args, **kwargs):
    return ExtendRandClassDecoratorImpl(target, args, kwargs)

def randclass(*args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # No-argument form
        return RandClassDecoratorImpl([], {})(args[0])
    else:
        return RandClassDecoratorImpl(args, kwargs)
    
def randobj(*args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # No-argument form
        return RandObjDecoratorImpl({})(args[0])
    else:
        return RandObjDecoratorImpl(kwargs)
    
    
