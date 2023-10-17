import datetime as dt
import re
from typing import List, cast


class DateTimeConverter:
    # When adding pattern here put the pattern with most information on top
    _patterns = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d"]
    utc_offset_re = re.compile(r"([\+-])(\d+)$")
    multiSpace_re = re.compile(r"( {2,})")

    @classmethod
    def convertDateTime(cls, entry: str):
        entry = re.sub(cls.multiSpace_re, " ", entry)
        match = cls.utc_offset_re.search(entry)
        if match and len(match.group(2)) == 3:
            entry = entry.replace(match.group(0), match.group(1) + "0" + match.group(2))

        dates: List[dt.datetime] = []
        for pattern in set(cast(List[str], cls._patterns)):
            try:
                dates.append(dt.datetime.strptime(entry, pattern))
            except:
                continue

        return dates[0] if len(dates) > 0 else None
