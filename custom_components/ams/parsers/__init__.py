
from ..const import AIDON_METER_SEQ, KAIFA_METER_SEQ, KAMSTRUP_METER_SEQ


def auto_detect_parser(pkg):
    """Helper to detect meter manufacturer."""
    if pkg == "kamstrup":
        pkg = KAMSTRUP_METER_SEQ
    elif pkg == "aidon":
        pkg = AIDON_METER_SEQ
    elif pkg == "kaifa":
        pkg = KAIFA_METER_SEQ

    for i in range(len(pkg)):
        if pkg[i] == AIDON_METER_SEQ[0] and pkg[i:i + len(AIDON_METER_SEQ)] == AIDON_METER_SEQ:
            from . import aidon
            return aidon
        elif pkg[i] == KAIFA_METER_SEQ[0] and pkg[i:i + len(KAIFA_METER_SEQ)] == KAIFA_METER_SEQ:
            from . import kaifa
            return kaifa
        elif pkg[i] == KAMSTRUP_METER_SEQ[0] and pkg[i:i + len(KAMSTRUP_METER_SEQ)] == KAMSTRUP_METER_SEQ:
            from . import kamstrup
            return kamstrup

    return None
