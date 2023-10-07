from ecl2df import common

_old_parse_ecl_month = common.parse_ecl_month


def _patched_parse_ecl_month(eclmonth):
    return _old_parse_ecl_month(eclmonth.upper()[:3])


common.parse_ecl_month = _patched_parse_ecl_month
