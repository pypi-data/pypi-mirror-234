from datetime import datetime
from typing import Optional

from ..general.Constants import DATE_FORMAT


class SECUnits:
    unit: str
    start: Optional[datetime]
    end: datetime
    val: int
    accn: str
    year: int
    quarter: str
    form_type: str
    date_filed: datetime
    frame: str

    def __init__(self, end: str, val: int, accn: str, fy: int, fp: str, form: str, filed: str,
                 unit: str, frame: str = "", start: Optional[str] = None):
        self.end = datetime.strptime(end, DATE_FORMAT)
        self.date_filed = datetime.strptime(filed, DATE_FORMAT)
        self.val = val
        self.accn = accn
        self.year = fy
        self.quarter = fp
        self.form_type = form
        self.unit = unit
        self.frame = frame
        self.start = datetime.strptime(start, DATE_FORMAT) if start is not None else start

    def to_dict(self):
        return self.__dict__
