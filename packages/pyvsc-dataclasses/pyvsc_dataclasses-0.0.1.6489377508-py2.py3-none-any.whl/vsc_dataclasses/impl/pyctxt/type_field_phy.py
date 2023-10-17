
import vsc_dataclasses.impl.context as ctxt_api
from .val_ref import ValRef
from .type_field import TypeField



class TypeFieldPhy(ctxt_api.TypeFieldPhy, TypeField):

    def __init__(self, name, dtype, attr, init):
        TypeField.__init__(self, name, dtype, attr)
        self._init = init

    def getInit(self) -> 'ValRef':
        return self._init
    
    def accept(self, v):
        v.visitTypeFieldPhy(self)
