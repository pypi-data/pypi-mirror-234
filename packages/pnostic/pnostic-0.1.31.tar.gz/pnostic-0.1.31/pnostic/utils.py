import datetime
import type_enforced


def fancy_date(date: datetime.datetime) -> str:
	return date.strftime("%a %b %d %H:%M:%S %Z %Y")

def now() -> datetime.datetime:
    current:datetime.datetime = datetime.datetime.now(datetime.datetime.utc)
    current.str = lambda:fancy_date(current)
    return current