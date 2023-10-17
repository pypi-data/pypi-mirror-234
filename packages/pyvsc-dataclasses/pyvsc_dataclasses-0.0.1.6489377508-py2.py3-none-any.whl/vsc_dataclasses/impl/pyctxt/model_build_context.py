
import vsc_dataclasses.impl.context as ctxt_api

class ModelBuildContext(ctxt_api.ModelBuildContext):

    def __init__(self, ctxt):
        self._ctxt = ctxt

    def ctxt(self) -> 'Context':
        return self._ctxt