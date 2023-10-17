
import vsc_dataclasses.impl.context as ctxt_api
from vsc_dataclasses.impl.pyctxt.model_field import ModelField

class DataTypeInt(ctxt_api.DataType):

    def __init__(self, is_signed : bool, width : int):
        self._is_signed = is_signed
        self._width = width

    def is_signed(self):
        return self._is_signed

    def width(self):
        return self._width

    def mkRootField(self,
        ctxt : 'ModelBuildContext',
        name : str,
        is_ref : bool) -> 'ModelField':
        raise NotImplementedError("mkRootField")

    def mkTypeField(self,
        ctxt : 'ModelBuildContext',
        type : 'TypeField') -> 'ModelField':
        ret = ModelField(
            type.name(),
            type.getDataType())
        ret._val.setBits(self._width)
        
        return ret
    
    def accept(self, v):
        v.visitDataTypeInt(self)

    pass