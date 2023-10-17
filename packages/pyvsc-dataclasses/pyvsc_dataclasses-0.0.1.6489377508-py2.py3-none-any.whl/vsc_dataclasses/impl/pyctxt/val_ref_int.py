#****************************************************************************
#* val_ref_int.py
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
from .val_ref import ValRef
    
class ValRefInt(ValRef):
    
    def __init__(self, val, type):
        super().__init__(val, type)

    def bits(self) -> int:
        return self._type.width()
    
    def is_signed(self) -> bool:
        return self._type.is_signed()
    
    def get_val_s(self) -> int:
        return self._val

    def get_val_u(self) -> int:
        return self._val
    
    def set_val(self, v):
        self._val = v

