
import vsc_dataclasses.impl.context as ctxt_api

class TypeField(ctxt_api.TypeField):

    def __init__(self, name, dtype, attr):
        self._name = name
        self._dtype = dtype
        self._attr = attr
        self._parent = None
        self._index = -1

    def getParent(self) -> 'TypeField':
        return self._parent

    def setParent(self, p : 'TypeField'):
        self._parent = p

    def getIndex(self) -> int:
        return self._index

    def setIndex(self, idx : int):
        self._index = idx

    def getDataType(self) -> 'DataType':
        return self._dtype

    def setDataType(self, dtype : 'DataType'):
        self._dtype = dtype

    def name(self) -> str:
        return self._name

    def mkModelField(self, ctxt : 'ModelBuildContext') -> 'ModelField':
        return self._dtype.mkTypeField(ctxt, self)
    
    def accept(self, v):
        v.visitTypeField(self)
