from typing import List
from wcd_locales_collector.services import pathifier


class _AutoextendedList(list):
    _extended: bool

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._extended = False

    def __iter__(self):
        self._extend()
        return super().__iter__()

    def __len__(self):
        self._extend()
        return super().__len__()

    def __reversed__(self):
        self._extend()
        return super().__reversed__()

    def _extend(self):
        if self._extended:
            return

        try:
            from wcd_locales_collector.conf import settings
        except AssertionError as e:
            return

        self._extended = True

        if not settings.PATH or len(settings.MODULES) < 1:
            return

        for path in pathifier.get_modules_result_paths(
            settings.MODULES, settings.PATH
        ):
            if path not in self:
                self.append(path)


def locale_paths_extender(paths: List[str]) -> List[str]:
    """
    Extend locale paths with locations collected paths.
    """
    return _AutoextendedList(paths)
