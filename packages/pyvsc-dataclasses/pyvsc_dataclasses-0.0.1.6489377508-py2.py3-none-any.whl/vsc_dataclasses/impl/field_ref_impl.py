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
from .modelinfo import ModelInfo


class FieldRefImpl(object):

    def __init__(self, name, idx):
        self.target = None
        self._modelinfo = ModelInfo(self, name, None)
        self._modelinfo._idx = idx
        self._modelinfo._is_ref = True
        pass

    def get_val(self, modelinfo_p):
        print("get_val")
        this_f = modelinfo_p.libobj.getField(self._modelinfo._idx)
        print("this_f: %s" % str(this_f))
        target = this_f.getRef()

        if target is None:
            raise Exception("Attempting a null-reference dereference")
        
        return target.getFieldData()

    def set_val(self, lib_obj_p, val):
        print("FieldRefImpl.set_val")
        self.target = val
