#****************************************************************************
#* type_utils.py
#*
#* Copyright 2022 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#* Created on:
#*     Author: 
#*
#****************************************************************************
from typeworks.impl.typeinfo import TypeInfo as TwTypeInfo
from .ctor import Ctor
from .list_t import ListT
from .scalar_t import ScalarT
from .typeinfo_randclass import TypeInfoRandClass
from .typeinfo_scalar import TypeInfoScalar


class TypeUtils(object):

    def __init__(self):
        pass

    def val2TypeInfo(self, value):
        ctor = Ctor.inst()

        if issubclass(value, ScalarT):
            dt = ctor.ctxt().findDataTypeInt(value.S, value.W)
            return TypeInfoScalar(dt)
        elif issubclass(value, ListT):
            pass
        else:
            cls_ti_t = TwTypeInfo.get(value, False)

            if cls_ti_t is None:
                raise Exception("Type %s is not a VSC type" % str(value))
            
            return TypeInfoRandClass.get(cls_ti_t)

