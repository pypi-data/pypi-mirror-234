import epics


def epics_put(channel, value):
    epics.caput(channel, value)


def epics_get(channel):
    return epics.caget(channel)


def fshon():
    pass


def fshopen():
    """open the fast shutter"""
    epics_put("X12SA-ES1-TTL:OUT_01", 1)


def fshclose():
    """close the fast shutter"""
    epics_put("X12SA-ES1-TTL:OUT_01", 0)


def fshstatus():
    """show the fast shutter status"""
    return epics_get("X12SA-ES1-TTL:OUT_01")
