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
# Created on Apr 7, 2022
# 
# @author: mballance
#****************************************************************************

from .context import ModelFieldFlag
from .ctor import Ctor

class ModelInfo(object):
    
    def __init__(self, obj, name, typeinfo, idx=-1):
        self._obj = obj # User-facade object
        self._name = name
        self._typeinfo = typeinfo
        self._idx = idx
        self._libobj = None # Native object for the root of a data-structure tree
        self._parent = None
        self._randstate = None
        self._subfield_modelinfo = []
        self._is_topdown_scope = True
        self._is_ref = False

    @property
    def obj(self):
        return self._obj

    @obj.setter
    def obj(self, v):
        self._obj = v

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, v):
        self._name = v

    @property
    def info(self):
        return self._typeinfo

    @property
    def idx(self):
        return self._idx

    @idx.setter
    def idx(self, v):
        self._idx = v

    @property
    def libobj(self):
        return self._libobj

    @libobj.setter
    def libobj(self, v):
        self._libobj = v
        
    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, p):
        self._parent = p
        
    def addSubfield(self, subfield_mi):
        subfield_mi.parent = self
        self._subfield_modelinfo.append(subfield_mi)
        
    def pre_randomize(self):
        if hasattr(self._obj, "pre_randomize"):
            self._obj.pre_randomize()
        for field_mi in self._subfield_modelinfo:
            field_mi.pre_randomize()
            
    def post_randomize(self):
        if hasattr(self._obj, "post_randomize"):
            self._obj.post_randomize()
        for field_mi in self._subfield_modelinfo:
            field_mi.post_randomize()
        
    def set_rand(self):
        self._lib_obj.setFlag(ModelFieldFlag.DeclRand)
        
        
