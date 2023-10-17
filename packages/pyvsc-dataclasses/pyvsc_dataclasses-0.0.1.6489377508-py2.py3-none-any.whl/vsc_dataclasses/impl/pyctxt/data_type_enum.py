
import vsc_dataclasses.impl.context as ctxt_api

class DataTypeEnum(ctxt_api.DataType):

    def __init__(self, name, is_signed):
        self._name = name
        self._is_signed = is_signed
        self._enums = []
        self._enum_m = []

    def name(self) -> str:
        return self._name

    def isSigned(self) -> bool:
        return self._is_signed

    def addEnumerator(self, name, val : 'ModelVal') -> bool:
        if name not in self._enum_m.keys():
            self._enums.append(name)
            self._enum_m[name] = val
        else:
            return False

    def getDomain(self) -> 'TypeExprRangelist':
        raise NotImplementedError("getDomain")
