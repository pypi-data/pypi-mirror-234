import platform
import struct
import subprocess
from datetime import datetime, timedelta

import pytz

FILTER_SEARCH_USERS = "(&(objectCategory=person)(objectclass=user))"
FILTER_SEARCH_USER_BY_SAMACC = FILTER_SEARCH_USERS[:-1] + "(sAMAccountName={username}))"
FILTER_SEARCH_GROUPS = "(&(objectclass=group))"
FILTER_SEARCH_GROUP_BY_DN = "(&(objectclass=group)(dn={dn}))"


def sid_to_str(sid: bytes) -> str:
    """Converts a hexadecimal string returned from the LDAP query to a
    string version of the SID in format of S-1-5-21-1270288957-3800934213-3019856503-500

    ref: https://gist.github.com/mprahl/e38a2eba6da09b2f6bd69d30fd3b749e
    """
    revision = sid[0]
    number_of_sub_ids = sid[1]
    iav = struct.unpack(">Q", b"\x00\x00" + sid[2:8])[0]
    sub_ids = [
        struct.unpack("<I", sid[8 + 4 * i : 12 + 4 * i])[0] for i in range(number_of_sub_ids)
    ]
    return "S-{}-{}-{}".format(revision, iav, "-".join([str(sub_id) for sub_id in sub_ids]))


def winntformat_to_datetime(winntformat, timezone: str = "Europe/Rome") -> datetime:
    timestamp = float(winntformat)
    seconds_since_epoch = timestamp / 10**7
    loc_dt = datetime.fromtimestamp(seconds_since_epoch)
    loc_dt -= timedelta(days=(1970 - 1601) * 365 + 89)
    return pytz.timezone(timezone).localize(loc_dt)


def ping(host=None, retry_packets=1):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, str(retry_packets), host]
    return subprocess.call(command) == 0
