#****************************************************************************
#* list_tt_meta.py
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

from .list_t_meta import ListTMeta

class ListTTMeta(type):

    def __init__(self, name, bases, dct):
        super().__init__(name, bases, dct)
        self.bases = bases
        self.dct = dct
        self.type_m = {}

    def __getitem__(self, item):
        from .list_t import ListT

        if item in self.type_m.keys():
            return self.type_m[item]
        else:
            try:
                item_i = int(item)
            except Exception as e:
                raise Exception("Array dimension (%s) is not an integer" % str(item))

            DIM = self.dct["DIM"].copy()
            DIM.append(item_i)

            t = ListTTMeta("%s[%d]" % (self.__name__, item_i), (ListT,), 
                dict(T=self.dct["T"], DIM=DIM))

            t.T = self.dct["T"]
            t.DIM = DIM.copy()

        return t

