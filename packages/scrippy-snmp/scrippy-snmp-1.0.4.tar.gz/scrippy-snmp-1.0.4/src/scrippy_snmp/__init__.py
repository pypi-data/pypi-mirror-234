import logging
from pysnmp.proto.rfc1902 import Null, Bits, Integer32, OctetString, IpAddress, Counter32, Counter64, Gauge32, Unsigned32, TimeTicks

logger = logging.getLogger("scrippy.main")

VERSIONS = {"v1": 0, "1": 0,
            "2": 1, "v2": 1, "v2c": 1, "2c": 1,
            "v3": 2, "3": 2}


DATATYPES = {"null": Null,
             "bits": Bits,
             "int": Integer32,
             "str": OctetString,
             "ipaddr": IpAddress,
             "counter": Counter32,
             "counter64": Counter64,
             "gauge": Gauge32,
             "unisgned": Unsigned32,
             "ticks": TimeTicks}


class ScrippySnmpError(Exception):
  """Specifi error class"""

  def __init__(self, message):
    self.message = message
    super().__init__(self.message)
