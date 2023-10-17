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
#*
#* Declares back-end interface API and associated data types
#****************************************************************************
from enum import IntEnum, IntFlag, auto
from typing import Callable, List


class BinOp(IntEnum):
    Eq      = 0
    Ne      = auto()
    Gt      = auto()
    Ge      = auto()
    Lt      = auto()
    Le      = auto()
    Add     = auto()
    Sub     = auto()
    Div     = auto()
    Mul     = auto()
    Mod     = auto()
    BinAnd  = auto()
    BinOr   = auto()
    LogAnd  = auto()
    LogOr   = auto()
    Sll     = auto()
    Srl     = auto()
    Xor     = auto()
    Not     = auto()

class UnaryOp(IntEnum):
    pass

class CompoundSolver(object):

    def solve(self, rs : 'RandState', fields, constraints, flags):
        raise NotImplementedError("solve")

class DataType(object):
    def mkRootField(self,
        ctxt : 'ModelBuildContext',
        name : str,
        is_ref : bool) -> 'ModelField':
        raise NotImplementedError("mkRootField")

    def mkTypeField(self,
        ctxt : 'ModelBuildContext',
        type : 'TypeField') -> 'ModelField':
        raise NotImplementedError("mkTypeField")

class DataTypeEnum(DataType):
    def name(self) -> str:
        raise NotImplementedError("name")

    def isSigned(self) -> bool:
        raise NotImplementedError("isSigned")

    def addEnumerator(self, name, val : 'ValRef') -> bool:
        raise NotImplementedError("addEnumerator")

    def getDomain(self) -> 'TypeExprRangelist':
        raise NotImplementedError("getDomain")

class DataTypeInt(DataType):
    pass

class DataTypeList(DataType):

    def getElemType(self):
        raise NotImplementedError("getElemType")
    
class DataTypeListFixedSize(DataTypeList):

    def getSize(self):
        raise NotImplementedError("getSize")

class DataTypeStruct(DataType):

    def name(self) -> str:
        raise NotImplementedError("name")

    def addField(self, f : 'TypeField'):
        raise NotImplementedError("addField unimplemented for %s" % str(type(self)))

    def getFields(self) -> List['TypeField']:
        raise NotImplementedError("getFields")

    def getField(self, idx : int) -> 'TypeField':
        raise NotImplementedError("getField")

    def addConstraint(self, c : 'TypeConstraint'):
        raise NotImplementedError("addConstraint")

    def getConstraints(self) -> List['TypeConstraint']:
        raise NotImplementedError("getConstraints")

    def setCreateHook(self, hook : Callable):
        raise NotImplementedError("setCreateHook")

class ModelFieldFlag(IntFlag):
    NoFlags  = 0
    DeclRand = (1 << 0)
    UsedRand = (1 << 1)
    Resolved = (1 << 2)
    VecSize  = (1 << 3)

class ModelField(object):

    def name(self) -> str:
        raise NotImplementedError("name")

    def getDataType(self) -> DataType:
        raise NotImplementedError("getDataType")
    
    def getParent(self) -> 'ModelField':
        raise NotImplementedError("getParent")

    def setParent(self, parent : 'ModelField'):
        raise NotImplementedError("setParent")

    def constraints(self) -> List['ModelConstraint']:
        raise NotImplementedError("constraints")
    
    def addConstraint(self, c : 'ModelConstraint'):
        raise NotImplementedError("addConstraint")

    def fields(self) -> List['ModelField']:
        raise NotImplementedError("fields")

    def addField(self, f : 'ModelField'):
        raise NotImplementedError("addField")

    def getField(self, idx : int) -> 'ModelField':
        raise NotImplementedError("getField")

    def val(self) -> 'ValRef':
        raise NotImplementedError("val")

    def clearFlag(self, flags : 'ModelFieldFlag'):
        raise NotImplementedError("clearFlag")

    def setFlag(self, flags : 'ModelFieldFlag'):
        raise NotImplementedError("setFlag")

    def isFlagSet(self, flags : 'ModelFieldFlag') -> bool:
        raise NotImplementedError("isFlagSet")

    def setFieldData(self, data):
        raise NotImplementedError("setFieldData")

    def getFieldData(self) -> object:
        raise NotImplementedError("getFieldData")



class ValRef(object):

    def type(self) -> DataType:
        raise NotImplementedError("type")
    
class ValRefInt(ValRef):

    def bits(self) -> int:
        raise NotImplementedError("bits")
    
    def is_signed(self) -> bool:
        raise NotImplementedError("is_signed")
    
    def get_val_s(self) -> int:
        raise NotImplementedError("get_val_s")

    def get_val_u(self) -> int:
        raise NotImplementedError("get_val_u")
    
    def set_val(self, v):
        raise NotImplementedError("set_val")


class ModelBuildContext(object):

    def ctxt(self) -> 'Context':
        raise NotImplementedError("ctxt")

class RandState(object):

    def seed(self) -> str:
        raise NotImplementedError("seed")

    def randint32(self, low, high):
        raise NotImplementedError("randint32")

    def randbits(self, v : 'ModelVal'):
        raise NotImplementedError("randbits")

    def setState(self, other : 'RandState'):
        raise NotImplementedError("setState")

    def clone(self) -> 'RandState':
        raise NotImplementedError("clone")

    def next(self) -> 'RandState':
        raise NotImplementedError("next")
    
class TypeConstraint(object):
    pass

class TypeConstraintForeach(TypeConstraint):

    def getTarget(self) -> 'TypeExpr':
        raise NotImplementedError("TypeConstraintForeach.getTarget")

    def getBody(self) -> TypeConstraint:
        raise NotImplementedError("TypeConstraintForeach.getBody")
    
class TypeConstraintScope(object):

    def getConstraints(self):
        raise NotImplementedError("getConstraints")
    
    def addConstraint(self, c):
        raise NotImplementedError("addConstraint")

class SolveFlags(IntEnum):
    pass

class TypeFieldAttr(IntFlag):
    NoAttr = 0
    Rand = (1 << 0)

#********************************************************************
#* TypeExpr
#********************************************************************

class TypeExpr(object):
    pass

class TypeExprFieldRefKind(IntEnum):
    TopDownScope = auto()
    BottomUpScope = auto()

#class TypeExprFieldRefElem(object):
#    kind : TypeExprFieldRefElemKind
#    idx : int

class TypeExprBin(TypeExpr):

    def lhs(self):
        raise NotImplementedError("lhs")
    
    def op(self):
        raise NotImplementedError("op")

    def rhs(self):
        raise NotImplementedError("rhs")

class TypeExprFieldRef(TypeExpr):

    def getRootExpr(self):
        raise NotImplementedError("getRootExpr")
    
    def getRootRefKind(self):
        raise NotImplementedError("getRootRefKind")
    
    def getRootRefOffset(self):
        raise NotImplementedError("getRootRefOffset")
    
    def addPathElem(self, idx):
        raise NotImplementedError("addPathElem")
    
    def size(self):
        raise NotImplementedError("size")
    
    def at(self):
        raise NotImplementedError("at")
    
    def getPath(self):
        raise NotImplementedError("getPath")


class TypeExprRange(TypeExpr):

    def isSingle(self) -> bool:
        raise NotImplementedError("isSingle")

    def lower(self) -> 'TypeExpr':
        raise NotImplementedError("lower")

    def upper(self) -> 'TypeExpr':
        raise NotImplementedError("upper")

class TypeExprVal(TypeExpr):

    def val(self) -> 'ValRef':
        raise NotImplementedError("val")

#********************************************************************
#* TypeField
#********************************************************************

class TypeField(object):

    def getParent(self) -> 'TypeField':
        raise NotImplementedError("getParent")

    def setParent(self, p : 'TypeField'):
        raise NotImplementedError("setParent")

    def getIndex(self) -> int:
        raise NotImplementedError("getIndex")

    def setIndex(self, idx : int):
        raise NotImplementedError("setIndex")

    def getDataType(self) -> 'DataType':
        raise NotImplementedError("getDataType")

    def name(self) -> str:
        raise NotImplementedError("name")

    def mkModelField(self, ctxt : 'ModelBuildContext') -> 'ModelField':
        raise NotImplementedError("mkModelField")


class TypeFieldPhy(TypeField):

    def getInit(self) -> 'ValRef':
        raise NotImplementedError('getInit')

class TypeFieldRef(TypeField):
    pass



class Context(object):

    def findDataTypeEnum(self, name) -> DataTypeEnum:
        raise NotImplementedError("findDataTypeEnum")

    def mkDataTypeEnum(self, name) -> DataTypeEnum:
        raise NotImplementedError("mkDataTypeEnum")

    def addDataTypeEnum(self, t : DataTypeEnum) -> bool:
        raise NotImplementedError("addDataTypeEnum")

    def findDataTypeInt(self, is_signed : bool, width : int) -> DataTypeInt:
        raise NotImplementedError("findDataTypeInt")

    def mkDataTypeInt(self, is_signed : bool, width : int, create : bool=True) -> DataTypeInt:
        raise NotImplementedError("mkDataTypeInt")

    def addDataTypeInt(self, t : DataTypeInt) -> bool:
        raise NotImplementedError("addDataTypeInt")
    
    def findDataTypeList(self, t : DataType, create : bool=True) -> DataTypeList:
        raise NotImplementedError("findDataTypeList")
    
    def mkDataTypeList(self, t : DataType, owned : bool) -> DataTypeList:
        raise NotImplementedError("mkDataTypeList")
    
    def addDataTypeList(self, t : DataTypeList):
        raise NotImplementedError("addDataTypeList")

    def findDataTypeListFixedSize(self, t : DataType, sz, create : bool=True) -> DataTypeListFixedSize:
        raise NotImplementedError("findDataTypeListFixedSize")
    
    def mkDataTypeListFixedSize(self, t : DataType, owned : bool, sz) -> DataTypeListFixedSize:
        raise NotImplementedError("mkDataTypeListFixedSize")
    
    def addDataTypeListFixedSize(self, t : DataTypeListFixedSize):
        raise NotImplementedError("addDataTypeListFixedSize")

    def findDataTypeStruct(self, name) -> DataTypeStruct:
        raise NotImplementedError("findDataTypeStruct")

    def mkDataTypeStruct(self, name) -> DataTypeStruct:
        raise NotImplementedError("mkDataTypeStruct")

    def addDataTypeStruct(self, t : DataTypeStruct) -> bool:
        raise NotImplementedError("addDataTypeStruct")

    def mkRandState(self, seed : str) -> RandState:
        raise NotImplementedError("mkRandState")

    def mkModelBuildContext(self, ctxt : 'Context') -> ModelBuildContext:
        raise NotImplementedError("mkModelBuildContext")

    def mkTypeConstraintBlock(self, name) -> 'TypeConstraintBlock':
        raise NotImplementedError("mkTypeConstraintBlock")

    def mkTypeConstraintExpr(self, e : 'TypeExpr') -> 'TypeConstraintExpr':
        raise NotImplementedError("mkTypeConstraintExpr")

    def mkTypeConstraintForeach(self, target_e : 'TypeExpr', body_c) -> 'TypeConstraintForeach':
        raise NotImplementedError("mkTypeConstraintForeach")

    def mkTypeConstraintIfElse(self, c : 'TypeExpr', ct : 'TypeConstraint') -> 'TypeConstraintIfElse':
        raise NotImplementedError("mkTypeConstraintIfElse")

    def mkTypeConstraintImplies(self, c : 'TypeExpr', b : 'TypeConstraint') -> 'TypeConstraintImplies':
        raise NotImplementedError("mkTypeConstraintImplies")

    def mkTypeConstraintScope(self) -> 'TypeConstraintScope':
        raise NotImplementedError("mkTypeConstraintScope")

    def mkTypeConstraintSoft(self, c : 'TypeConstraintExpr') -> 'TypeConstraintSoft':
        raise NotImplementedError("mkTypeConstraintSoft")

    def mkTypeConstraintUnique(self, e : List['TypeExpr']) -> 'TypeConstraintUnique':
        raise NotImplementedError("mkTypeConstraintUnique")

    def mkTypeExprBin(self, lhs : 'TypeExpr', op : BinOp, rhs : 'TypeExpr') -> 'TypeExprBin':
        raise NotImplementedError("mkTypeExprBin")

    def mkTypeExprFieldRef(self, kind, offset, path) -> 'TypeExprFieldRef':
        raise NotImplementedError("mkTypeExprFieldRef")

    def mkTypeExprRange(self,
        is_single : bool,
        lower : 'TypeExpr',
        upper : 'TypeExpr') -> 'TypeExprRange':
        raise NotImplementedError("mkTypeExprRange")

    def mkTypeExprRangelist(self):
        raise NotImplementedError("mkTypeExprRangelist")

    def mkTypeExprVal(self, val : 'ValRef'):
        raise NotImplementedError("mkTypeExprVal")

    def mkTypeFieldPhy(self,
        name,
        dtype : 'DataType',
        own_dtype : bool,
        attr,
        init : 'ValRef') -> 'TypeFieldPhy':
        raise NotImplementedError("mkTypeFieldPhy")

    def mkTypeFieldRef(self,
        name,
        dtype : 'DataType',
        attr) -> 'TypeFieldRef':
        raise NotImplementedError("mkTypeFieldRef")
    
    def mkValRefInt(self, value, is_signed, width):
        raise NotImplementedError("mkValRef")

