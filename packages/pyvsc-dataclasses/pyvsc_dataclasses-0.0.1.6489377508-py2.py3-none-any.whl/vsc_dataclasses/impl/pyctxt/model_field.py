
from typing import List
import vsc_dataclasses.impl.context as ctxt_api
from .val_ref import ValRef

class ModelField(ctxt_api.ModelField):

    def __init__(self, name, dt):
        self._name = name
        self._dt = dt
        self._parent = None
        self._constraints = []
        self._fields = []
        self._val = None
        self._flags = 0
        self._data = None

    def name(self) -> str:
        raise NotImplementedError("name")

    def getDataType(self) -> 'DataType':
        return self._dt
    
    def getParent(self) -> 'ModelField':
        return self._parent

    def setParent(self, parent : 'ModelField'):
        self._parent = parent

    def constraints(self) -> List['ModelConstraint']:
        return self._constraints
    
    def addConstraint(self, c : 'ModelConstraint'):
        self._constraints.append(c)

    def fields(self) -> List['ModelField']:
        return self._fields

    def addField(self, f : 'ModelField'):
        self._fields.append(f)

    def getField(self, idx : int) -> 'ModelField':
        return self._fields[idx]

    def val(self) -> 'ValRef':
        return self._val

    def clearFlag(self, flags : 'ModelFieldFlag'):
        raise NotImplementedError("clearFlag")

    def setFlag(self, flags : 'ModelFieldFlag'):
        raise NotImplementedError("setFlag")

    def isFlagSet(self, flags : 'ModelFieldFlag') -> bool:
        raise NotImplementedError("isFlagSet")

    def setFieldData(self, data):
        self._data = data

    def getFieldData(self) -> object:
        return self._data
