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
#****************************************************************************
from .ctor import Ctor
from .modelinfo import ModelInfo

class CompositeValClosure(object):

    def __init__(self, obj, modelinfo_p : ModelInfo):
        self.obj = obj
        self.modelinfo_p = modelinfo_p

    def __getattribute__(self, name: str):
        print("Closure::__getattribute__ %s" % name)
        ctor = Ctor.inst()
        ret = object.__getattribute__(obj, name)

        if not ctor.raw_mode():
            ctor.push_raw_mode()
            if ctor.expr_mode():
                pass
            elif hasattr(ret, "get_val"):
                print("Closure:: replacing with get_val")
                ret = ret.get_val(self.modelinfo_p)
            ctor.pop_raw_mode()

        return ret

    # def __setattr__(self, name, value):
    #     print("CompositeValueClosure::__setattr__ %s %s" % (name, str(value)))
    # # def __setattr__(self, name: str, value):
    # #     print("CompositeValueClosure::__setattr__ %s" % name)
    # #     try:
    # #         obj = object.__getattribute__(self, "obj")
    # #     except:
    # #         object.__setattr__(self, name, value)
    # #     else:
    # #         try:
    # #             fo = object.__getattribute__(obj, name)
    # #         except:
    # #             object.__setattr__(obj, name, value)
    # #         else:
    # #             modelinfo_p = object.__getattribute__(self, "modelinfo_p")
    # #             if hasattr(fo, "set_val"):
    # #             fo.set_val(self.modelinfo_p, value)
