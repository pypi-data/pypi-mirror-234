from typing import Literal, Optional

from LOGS.Entities.Track import Track
from LOGS.Entities.TrackXYData import TrackXYData

TrackTypes = Literal[
    "nucleotide_sequence",
    "image",
    "matrix_real",
    "pdf",
    "table",
    "XY_complex",
    "XY_real",
]


class TrackXY(Track):
    _datatracks: Optional[TrackXYData] = None

    def _fetchData(self):
        if self.datatracks:
            if self.datatracks.x:
                self.datatracks.x.fetchFull()
            if self.datatracks.y:
                self.datatracks.y.fetchFull()

    def __iter__(self):
        if (
            self.datatracks is not None
            and self.datatracks.x is not None
            and self.datatracks.x.count is not None
            and self.datatracks.x.data is not None
            and self.datatracks.y is not None
            and self.datatracks.y.count is not None
            and self.datatracks.y.data is not None
        ):
            for i in range(min(self.datatracks.x.count, self.datatracks.y.count)):
                yield self.datatracks.x.data[i], self.datatracks.y.data[i]

    @property
    def datatracks(self) -> Optional[TrackXYData]:
        return self._datatracks

    @datatracks.setter
    def datatracks(self, value):
        self._datatracks = self.checkAndConvertNullable(value, TrackXYData, "data")
