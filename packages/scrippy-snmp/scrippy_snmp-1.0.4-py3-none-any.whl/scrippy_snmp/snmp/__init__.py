#!/usr/bin/env python3
"""
This module provides SNMP interrogation capability to Scrippy.
"""
from pysnmp.entity.rfc3413.oneliner import cmdgen
from scrippy_snmp import ScrippySnmpError, logger, VERSIONS, DATATYPES


class Snmp:
  """SNMP object is used to connect to and query  remote host using SNMP."""
  def __init__(self, host, port, community, version, timeout=1, retries=3):
    logger.debug("[+] SNMP agent initialization")
    self.generator = cmdgen.CommandGenerator()
    self.host = host
    self.port = port
    self.community = self._set_community(community=community, version=version)
    self.transport = self._set_transport(timeout=1, retries=3)
    self.mib = None

  def get(self, oid):
    logger.debug(f"[+] Retrieving OID {oid}")
    error_indication, error_status, error_index, var_binds = self.generator.getCmd(self.community, self.transport, oid)
    if error_indication is None and error_status == 0:
      try:
        if len(var_binds) > 1:
          raise IndexError()
        return tuple(var_binds[0].prettyPrint().split(" = "))
      except IndexError as err:
        err_msg = f"Unexpected answer from remote host: {str(var_binds)}"
        raise ScrippySnmpError(err_msg) from err
    if error_indication is not None:
      err_msg = error_indication
    elif error_status > 0:
      err_index = "?"
      if error_index > 0:
        err_index = var_binds[int(error_index) - 1]
      err_msg = f"{error_status.prettyPrint()} at {err_index}"
    raise ScrippySnmpError(err_msg)

  def walk(self, oid=".1.3.6"):
    logger.debug(f"[+] Retrieving from OID {oid}")
    error_indication, error_status, error_index, var_binds = self.generator.nextCmd(self.community, self.transport, oid)
    if error_indication is None and error_status == 0:
      try:
        return [tuple(var[0].prettyPrint().split(" = ")) for var in var_binds]
      except IndexError as err:
        err_msg = f"Unexpected answer from remote host: {str(var_binds)}"
        raise ScrippySnmpError(err_msg) from err
    if error_indication is not None:
      err_msg = error_indication
    elif error_status > 0:
      err_index = "?"
      if error_index > 0:
        err_index = var_binds[int(error_index) - 1]
      err_msg = f"{error_status.prettyPrint(),} at {err_index}"
    raise ScrippySnmpError(err_msg)

  def set(self, oid, value, datatype):
    logger.debug(f"[+] Setting value to OID {oid} => {value}")
    data = self._get_datatype(datatype)(value)
    self.generator.setCmd(self.community, self.transport, (oid, data))

  def _set_community(self, community, version):
    logger.debug(f" '-> Setting community: {community} / Version: {version}")
    version = self._get_version(version)
    return cmdgen.CommunityData('server', community, version)

  def _set_transport(self, timeout=1, retries=3):
    logger.debug(f" '-> Setting transport: UDP: {self.host}:{self.port}")
    return cmdgen.UdpTransportTarget((self.host, self.port),
                                     timeout=timeout,
                                     retries=retries)

  def _get_datatype(self, datatype):
    try:
      return DATATYPES[datatype]
    except KeyError as err:
      err_msg = f"Unknown datatype: {datatype}"
      logger.critical(err_msg)
      raise ScrippySnmpError(err_msg) from err

  def _get_version(self, version):
    try:
      return VERSIONS[str(version)]
    except KeyError as err:
      err_msg = f"Unknown snmp version: {version}"
      logger.critical(err_msg)
      raise ScrippySnmpError(err_msg) from err
