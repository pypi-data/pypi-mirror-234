from typing import Optional

from LOGS.Entity.SerializeableContent import SerializeableContent


class HierarchyLeaf(SerializeableContent):
    _track: Optional[str] = None

    @property
    def track(self) -> Optional[str]:
        return self._track

    @track.setter
    def track(self, value):
        self._track = self.checkAndConvertNullable(value, str, "track")
