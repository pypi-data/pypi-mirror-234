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
# Created on Jun 23, 2022
#
# @author: mballance
#****************************************************************************
import dataclasses
from .import ctor
from .ctor import Ctor

class CovergroupDecoratorImpl(object):
    
    def __init__(self, kwargs):
        pass
    

    def __call__(self, T):
        Tp = dataclasses.dataclass(T, init=False)

        Ctor.inst().push_expr_mode()
        for f in dataclasses.fields(Tp):
            print("Field: %s" % f.name)
            if callable(f.type) and f.type != int:
                f.type(Tp)
        Ctor.inst().pop_expr_mode()

        pass    
