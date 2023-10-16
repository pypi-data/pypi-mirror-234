from LOGS.Entity.SerializeableContent import SerializeableContent


class TrackData(SerializeableContent):
    def fetchFull(self):
        raise NotImplementedError(
            "Specific %a class for this track type is not implemented yet."
            % type(self).__name__
        )
