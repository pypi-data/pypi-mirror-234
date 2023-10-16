from pathlib import Path, PurePath
from navconfig import config
from flowtask.utils import fnExecutor
from .log import LogSupport
from .env import EnvSupport

class MaskSupport(LogSupport, EnvSupport):

    _variables: dict

    def __init__(self, **kwargs):
        self._masks: dict = {}
        self._variables = kwargs.pop('variables', {})
        self._environment = config
        super(MaskSupport, self).__init__(**kwargs)
        # filling Masks:
        masks = kwargs.pop('masks', None)
        if masks:
            self._masks = masks
            object.__setattr__(self, 'masks', self._masks)
        self.process_masks()

    def process_masks(self):
        for mask, replace in self._masks.items():
            # first: making replacement of masks based on vars:
            try:
                if mask in self._variables:
                    value = self._variables[mask]
                else:
                    value = replace.format(**self._variables)
            except Exception:
                value = replace
            try:
                value = fnExecutor(value, env=self._environment)
                self._masks[mask] = value
            except Exception as err:
                self._logger.warning(f'Mask Error: {err}')

    def mask_replacement(self, obj):
        for mask, replace in self._masks.items():
            if mask in self._variables:
                value = self._variables[mask]
            else:
                value = str(obj).replace(mask, str(replace))
            if isinstance(obj, PurePath):
                obj = Path(value).resolve()
            else:
                obj = value
        return obj
