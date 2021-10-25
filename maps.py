from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

DT_PATTERN = "%Y-%m-%d"

TOOTH_MAP = {
    "permanent": [str(first) + str(second) for first in range(1, 5) for second in range(1, 9)],
    "primary": [str(first) + str(second) for first in range(5, 9) for second in range(1, 6)],
}


class DateRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end


TIME_INTERVAL_MAP = {
    "1 week": lambda x: datetime.strptime(x, DT_PATTERN).date() + timedelta(weeks=1),
    "2 weeks": lambda x: datetime.strptime(x, DT_PATTERN).date() + timedelta(weeks=2),
    "4 weeks": lambda x: datetime.strptime(x, DT_PATTERN).date() + timedelta(weeks=4),
    "6-8 weeks": lambda x: DateRange(
        start=datetime.strptime(x, DT_PATTERN).date() + timedelta(weeks=6),
        end=datetime.strptime(x, DT_PATTERN).date() + timedelta(weeks=8)
    ),
    "8 weeks": lambda x: datetime.strptime(x, DT_PATTERN).date() + timedelta(weeks=8),
    "3 months": lambda x: datetime.strptime(x, DT_PATTERN).date() + relativedelta(months=+3),
    "4 months": lambda x: datetime.strptime(x, DT_PATTERN).date() + relativedelta(months=+4),
    "6 months": lambda x: datetime.strptime(x, DT_PATTERN).date() + relativedelta(months=+6),
    "1 year": lambda x: datetime.strptime(x, DT_PATTERN).date() + relativedelta(years=+1),
    "Yearly up to 5 years": lambda x: [
        datetime.strptime(x, DT_PATTERN).date() + relativedelta(years=+y) for y in range(1, 6)
    ],
    "At 6 years old": lambda x: "At 6 years old",
}
