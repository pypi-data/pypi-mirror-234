
import datetime

def datetime2timestamp(d: datetime.datetime) -> str:
    result = d.isoformat(' ')
    if len(result) == 19:
        return result + '.000000'
    return result


def timedelta2str(td: datetime.timedelta) -> str:
    total_seconds = td.days * (24 * 60 * 60) + td.seconds
    microseconds = td.microseconds
    if td.days < 0:
        total_seconds = abs(total_seconds)
        if microseconds:
            total_seconds -= 1
            microseconds = 1000000 - microseconds
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if microseconds:
        result = "%d:%d:%d.%06d" % (hours, minutes, seconds, microseconds)
    else:
        result = "%d:%d:%d" % (hours, minutes, seconds)
    if td.days >= 0:
        return result
    return "-" + result



