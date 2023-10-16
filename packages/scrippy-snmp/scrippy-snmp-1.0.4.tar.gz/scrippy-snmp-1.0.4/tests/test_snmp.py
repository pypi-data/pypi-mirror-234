from scrippy_snmp import ScrippySnmpError
from scrippy_snmp.snmp import Snmp


HOST = "snmpd"
PORT = 161
RO_COMMUNITY = "ro-scrippy"
RW_COMMUNITY = "rw-scrippy"
VERSION = "2c"
LOCATION_OID = ".1.3.6.1.2.1.1.6.0"
EXPECTED_LOCATION = ("SNMPv2-MIB::sysLocation.0", "Unknown")


def test_get_snmp():
  """Get test"""
  snmp = Snmp(host=HOST, port=PORT, community=RO_COMMUNITY, version=VERSION)
  location = snmp.get(LOCATION_OID)
  assert location == EXPECTED_LOCATION


def test_oid_err():
  LOCATION_OID = ".1.3.6.1.2.1.1.6.42"
  EXPECTED = ("SNMPv2-MIB::sysLocation.42", "No Such Instance currently exists at this OID")
  snmp = Snmp(host=HOST, port=PORT, community=RO_COMMUNITY, version=VERSION)
  location = snmp.get(LOCATION_OID)
  assert location == EXPECTED


def test_community_err():
  RO_COMMUNITY = "err"
  snmp = Snmp(host=HOST, port=PORT, community=RO_COMMUNITY, version=VERSION)
  try:
    location = snmp.get(LOCATION_OID)
    assert location == EXPECTED_LOCATION
  except ScrippySnmpError as err:
    assert str(err) == "No SNMP response received before timeout"
    return
  raise Exception("Failed: test_community_err()")


def test_version():
  VERSION = 42
  try:
    snmp = Snmp(host=HOST, port=PORT, community=RO_COMMUNITY, version=VERSION)
    location = snmp.get(LOCATION_OID)
    assert location == EXPECTED_LOCATION
  except ScrippySnmpError as err:
    assert str(err) == f"Unknown snmp version: {VERSION}"
    return
  raise Exception("Failed: test_version()")


def test_walk():
  OID = "1.3.6.1.2.1.1.9.1.2"
  EXPECTED = [("SNMPv2-MIB::sysORID.1",
               "SNMP-FRAMEWORK-MIB::snmpFrameworkMIBCompliance"),
              ("SNMPv2-MIB::sysORID.2",
               "SNMP-MPD-MIB::snmpMPDCompliance"),
              ("SNMPv2-MIB::sysORID.3",
               "SNMP-USER-BASED-SM-MIB::usmMIBCompliance"),
              ("SNMPv2-MIB::sysORID.4",
               "SNMPv2-MIB::snmpMIB"),
              ("SNMPv2-MIB::sysORID.5",
               "SNMPv2-SMI::snmpModules.16.2.2.1"),
              ("SNMPv2-MIB::sysORID.6",
               "SNMPv2-SMI::mib-2.49"),
              ("SNMPv2-MIB::sysORID.7",
               "SNMPv2-SMI::mib-2.50"),
              ("SNMPv2-MIB::sysORID.8",
               "SNMPv2-SMI::mib-2.4"),
              ("SNMPv2-MIB::sysORID.9",
               "SNMPv2-SMI::snmpModules.13.3.1.3"),
              ("SNMPv2-MIB::sysORID.10",
               "SNMPv2-SMI::mib-2.92")]
  snmp = Snmp(host=HOST, port=PORT, community=RO_COMMUNITY, version=VERSION)
  result = snmp.walk(OID)
  assert result == EXPECTED


def test_walk_err():
  OID = "1.3.6.1.2.1.1.9.1.42"
  EXPECTED = list()
  snmp = Snmp(host=HOST, port=PORT, community=RO_COMMUNITY, version=VERSION)
  result = snmp.walk(OID)
  assert result == EXPECTED


def test_walk_community_err():
  RO_COMMUNITY = "err"
  OID = "1.3.6.1.2.1.1.9.1.2"
  EXPECTED = list()
  snmp = Snmp(host=HOST, port=PORT, community=RO_COMMUNITY, version=VERSION)
  try:
    result = snmp.walk(OID)
    assert result == EXPECTED
  except ScrippySnmpError as err:
    assert str(err) == "No SNMP response received before timeout"
    return
  raise Exception("Failed: test_community_err()")


def test_set():
  snmp = Snmp(host=HOST, port=PORT, community=RW_COMMUNITY, version=VERSION)
  EXPECTED_LOCATION = ("SNMPv2-MIB::sysLocation.0", "Room 42")
  snmp.set(oid=LOCATION_OID, value="Room 42", datatype="str")
  location = snmp.get(LOCATION_OID)
  assert location == EXPECTED_LOCATION


def test_set_err():
  pass
