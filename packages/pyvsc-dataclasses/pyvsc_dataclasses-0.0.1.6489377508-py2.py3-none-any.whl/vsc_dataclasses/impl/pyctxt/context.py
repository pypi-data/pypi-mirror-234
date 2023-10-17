
import vsc_dataclasses.impl as impl
from ..context import BinOp
from typing import List
from vsc_dataclasses.impl.pyctxt.type_field_phy import TypeFieldPhy
from vsc_dataclasses.impl.pyctxt.type_field_ref import TypeFieldRef
from .data_type_list import DataTypeList
from .data_type_list_fixed_size import DataTypeListFixedSize
from .data_type_struct import DataTypeStruct
from .data_type_enum import DataTypeEnum
from .data_type_int import DataTypeInt
from .model_build_context import ModelBuildContext
from .rand_state import RandState
from .type_constraint_block import TypeConstraintBlock
from .type_constraint_expr import TypeConstraintExpr
from .type_constraint_foreach import TypeConstraintForeach
from .type_constraint_scope import TypeConstraintScope
from .type_expr_bin import TypeExprBin
from .type_expr_field_ref import TypeExprFieldRef
from .type_expr_val import TypeExprVal
from .val_ref_int import ValRefInt


class Context(impl.Context):
    """Pure-python stub implementation of context"""

    def __init__(self):
        self._dt_struct_m = {}
        self._dt_enum_m = {}
        self._dt_sint_m = {}
        self._dt_uint_m = {}
        self._dt_list_m = {}
        self._dt_list_fixed_sz_m = {}

    def findDataTypeEnum(self, name) -> DataTypeEnum:
        if name in self._dt_enum_m.keys():
            return self._dt_enum_m[name]
        else:
            return None

    def mkDataTypeEnum(self, name) -> DataTypeEnum:
        return DataTypeEnum(name, True)

    def addDataTypeEnum(self, t : DataTypeEnum) -> bool:
        if t._name not in self._dt_enum_m.keys():
            self._dt_enum_m[t._name] = t
        else:
            return False
        return True

    def findDataTypeInt(self, is_signed : bool, width : int, create : bool=True) -> DataTypeInt:
        ret = None
        if is_signed:
            if width in self._dt_sint_m.keys():
                ret = self._dt_sint_m[width]
            elif create:
                ret = self.mkDataTypeInt(is_signed, width)
                self._dt_sint_m[width] = ret
        else:
            if width in self._dt_uint_m.keys():
                ret = self._dt_uint_m[width]
            elif create:
                ret = self.mkDataTypeInt(is_signed, width)
                self._dt_uint_m[width] = ret
        return ret

    def mkDataTypeInt(self, is_signed : bool, width : int) -> DataTypeInt:
        return DataTypeInt(is_signed, width)

    def addDataTypeInt(self, t : DataTypeInt) -> bool:
        if t._is_signed:
            if t._width in self._dt_sint_m.keys():
                return False
            else:
                self._dt_sint_m[t._width] = t
        else:
            if t._width in self._dt_uint_m.keys():
                return False
            else:
                self._dt_uint_m[t._width] = t
        return True
    
    def findDataTypeList(self, t, create : bool=True) -> DataTypeList:
        if t in self._dt_list_m.keys():
            return self._dt_list_m[t]
        elif create:
            list_t = DataTypeList(t)
            self._dt_list_m[t] = list_t
            return list_t
        else:
            return None
    
    def mkDataTypeList(self, t, owned : bool) -> DataTypeList:
        return DataTypeList(t)
    
    def addDataTypeList(self, t : DataTypeList):
        self._dt_list_m[t.getElemType()] = t

    def findDataTypeListFixedSize(self, t, sz, create : bool=True) -> DataTypeListFixedSize:
        if t in self._dt_list_fixed_sz_m.keys() and sz in self._dt_list_fixed_sz_m[t].keys():
            return self._dt_list_fixed_sz_m[t][sz]
        elif create:
            list_t = DataTypeListFixedSize(t, sz)
            if t not in self._dt_list_fixed_sz_m.keys():
                self._dt_list_fixed_sz_m[t] = {}
            self._dt_list_fixed_sz_m[t][sz] = list_t
            return list_t
        else:
            return None
    
    def mkDataTypeListFixedSize(self, t, owned : bool, sz) -> DataTypeListFixedSize:
        return DataTypeListFixedSize(t, sz)
    
    def addDataTypeListFixedSize(self, t : DataTypeListFixedSize):
        if t.getElemType() not in self._dt_list_fixed_sz_m.keys():
            self._dt_list_fixed_sz_m[t.getElemType()] = {}
        self._dt_list_fixed_sz_m[t.getElemType()][t.getSize()] = t

    def findDataTypeStruct(self, name) -> DataTypeStruct:
        if name in self._dt_struct_m.keys():
            return self._dt_struct_m[name]
        else:
            return None

    def mkDataTypeStruct(self, name) -> DataTypeStruct:
        return DataTypeStruct(name)

    def addDataTypeStruct(self, t : DataTypeStruct) -> bool:
        if t.name() not in self._dt_struct_m.keys():
            self._dt_struct_m[t.name()] = t
            return True
        else:
            return False

    def mkModelBuildContext(self, ctxt : 'Context') -> ModelBuildContext:
        return ModelBuildContext(ctxt)

    def mkRandState(self, seed : str) -> RandState:
        return RandState(seed)
    
    def mkTypeConstraintBlock(self, name) -> 'TypeConstraintBlock':
        return TypeConstraintBlock(name)

    def mkTypeConstraintExpr(self, e : 'TypeExpr') -> 'TypeConstraintExpr':
        return TypeConstraintExpr(e)

    def mkTypeConstraintForeach(self, 
                            target_e : 'TypeExpr',
                            body_c) -> 'TypeConstraintForeach':
        return TypeConstraintForeach(target_e, body_c)
    
    def mkTypeConstraintScope(self):
        return TypeConstraintScope()

    def mkTypeConstraintIfElse(self, c : 'TypeExpr', ct : 'TypeConstraint') -> 'TypeConstraintIfElse':
        raise NotImplementedError("mkTypeConstraintIfElse")

    def mkTypeConstraintImplies(self, c : 'TypeExpr', b : 'TypeConstraint') -> 'TypeConstraintImplies':
        raise NotImplementedError("mkTypeConstraintImplies")

    def mkTypeConstraintSoft(self, c : 'TypeConstraintExpr') -> 'TypeConstraintSoft':
        raise NotImplementedError("mkTypeConstraintSoft")

    def mkTypeConstraintUnique(self, e : List['TypeExpr']) -> 'TypeConstraintUnique':
        raise NotImplementedError("mkTypeConstraintUnique")

    def mkTypeExprBin(self, lhs : 'TypeExpr', op : BinOp, rhs : 'TypeExpr') -> 'TypeExprBin':
        return TypeExprBin(lhs, op, rhs)

    def mkTypeExprFieldRef(self, kind, offset, path) -> 'TypeExprFieldRef':
        return TypeExprFieldRef(kind, offset, path)

    def mkTypeExprVal(self, val) -> 'TypeExprVal':
        return TypeExprVal(val)

    def mkTypeFieldPhy(self,
        name,
        dtype : 'DataType',
        own_dtype : bool,
        attr,
        init : 'ModelVal') -> 'TypeFieldPhy':
        return TypeFieldPhy(name, dtype, attr, init)

    def mkTypeFieldRef(self,
        name,
        dtype : 'DataType',
        attr) -> 'TypeFieldRef':
        return TypeFieldRef(name, dtype, attr)
    
    def mkValRefInt(self, value, is_signed, width):
        t = self.findDataTypeInt(is_signed, width)
        return ValRefInt(value, t) 

