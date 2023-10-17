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
# Created on Feb 27, 2022
#
# @author: mballance
#****************************************************************************
from .ctor import Ctor
from .field_enum_impl import FieldEnumImpl
from .enum_info_mgr import EnumInfoMgr
from .typeinfo_enum import TypeInfoEnum
from .type_kind_e import TypeKindE


class EnumT(object):

    # Holds enum info in the case that a type declaration
    # was created
    EnumInfo = None
    
    def __new__(cls, e_t, i=-1):
        ctor = Ctor.inst()

        print("e_t: %s" % str(e_t))        
        # Need to grab the enum type info
        info = EnumInfoMgr.inst().getInfo(e_t)

        raise Exception("Need different approach to enum")        
#        lib_field = libvsc.Task_ModelBuildField(
#            ctor.ctxt(),
#            info.lib_obj,
#            "")
#        print("lib_field: %s" % str(lib_field))
        
        return FieldEnumImpl(
            "", 
            TypeInfoEnum(TypeKindE.Enum, info.lib_obj, info),
            lib_field)
    pass