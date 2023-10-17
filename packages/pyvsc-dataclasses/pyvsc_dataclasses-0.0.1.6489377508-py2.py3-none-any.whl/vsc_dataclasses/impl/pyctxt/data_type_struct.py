
import traceback
from typing import Callable, List
import vsc_dataclasses.impl.context as ctxt_api
from vsc_dataclasses.impl.pyctxt.model_field import ModelField

class DataTypeStruct(ctxt_api.DataTypeStruct):

    def __init__(self, name):
        self._name = name
        self._fields = []
        self._constraints = []
        self._create_h = None

    def name(self) -> str:
        return self._name

    def addField(self, f : 'TypeField'):
        self._fields.append(f)

    def getFields(self) -> List['TypeField']:
        return self._fields

    def getField(self, idx : int) -> 'TypeField':
        if idx < 0:
            raise Exception("getField with negative index %d" % idx)
        if idx >= len(self._fields):
            raise Exception("getField with out-of-bounds index %d (size=%d)" % (
                idx, len(self._fields)))
        return self._fields[idx]

    def addConstraint(self, c : 'TypeConstraint'):
        self._constraints.append(c)

    def getConstraints(self) -> List['TypeConstraint']:
        return self._constraints

    def setCreateHook(self, hook : Callable):
        self._create_h = hook

    def mkRootField(self,
        ctxt : 'ModelBuildContext',
        name : str,
        is_ref : bool) -> 'ModelField':
        ret = ModelField(name, self)

        # Build out fields
        for tf in self._fields:
            ret.addField(tf.mkModelField(ctxt))

        # TODO: build out constraints
        return ret

    def mkTypeField(self,
        ctxt : 'ModelBuildContext',
        type : 'TypeField') -> 'ModelField':
        raise NotImplementedError("mkTypeField")

    def accept(self, v):
        v.visitDataTypeStruct(self)    
