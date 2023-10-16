
![Build Status](https://drone-ext.mcos.nc/api/badges/scrippy/scrippy-snmp/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)


![Scrippy, my scrangourou friend](./scrippy-snmp.png "Scrippy, my scrangourou friend")

# `scrippy_snmp`

Basic *SNMP* capabilities for the [`Scrippy`](https://codeberg.org/scrippy) framework.

## Prerequisites

### Python modules

#### List of required modules

The modules listed below will be automatically installed.

- pysnmp
- pysnmp-mibs

## Installation

### Manual

```bash
git clone https://codeberg.org/scrippy/scrippy-snmp.git
cd scrippy-snmp
python -m pip install -r requirements.txt
make install
```

### With `pip`

```bash
pip install scrippy-snmp
```

### Usage

This module allows basic *SNMP* operations such as `get`, `walk` and `set`.

it supports *SNMP* version 1 and version 2.  Version 3 is still in depveloppment.

#### *SNMP* operations

##### Setup

As in shell *SNMP* implementation it is first needed to set the connection up, typically by providing the remote hostname or IP address, the *UDP* port on which join the host and the *community string* which is a sort of secret identifier that is allowed to perform some operations on the remote host.

```python
from scrippy_snmp.snmp import Snmp

HOST = "127.0.0.1"
PORT = 161
RO_COMMUNITY = "read-only-community"
RW_COMMUNITY = "read-write-community"
VERSION = "2c"

snmp = Snmp(host=HOST, port=PORT, community=RO_COMMUNITY, version=VERSION)
```

##### Get

The `get` operation allows to retrieve a specific *OID* value:

```python
LOCATION_OID = ".1.3.6.1.2.1.1.6.0"

snmp = Snmp(host=HOST, port=PORT, community=RO_COMMUNITY, version=VERSION)
location = snmp.get(LOCATION_OID)

print(location)
("SNMPv2-MIB::sysLocation.0", "Room 42")
```

The return value is a 2 elements *Tuple* containing:
- The *OID* in text format
- The *OID* value


##### Walk

The `walk` operation allow to retrieve a collection of *OID* value directly under the specified *OID*

```python
SYSTEM_OID = ".1.3.6.1.2.1.1"

snmp = Snmp(host=HOST, port=PORT, community=RO_COMMUNITY, version=VERSION)
result = snmp.walk(SYSTEM_OID)

for value in result:
  print(value)

('SNMPv2-MIB::sysDescr.0', 'arcadia.local.mcos.nc 1148685499 FreeBSD 13.2-RELEASE')
('SNMPv2-MIB::sysObjectID.0', 'SNMPv2-SMI::enterprises.12325.1.1.2.1.1')
('SNMPv2-MIB::sysUpTime.0', '320223')
('SNMPv2-MIB::sysContact.0', 'sysmeister@example.com')
('SNMPv2-MIB::sysName.0', 'scrippy.example.com')
('SNMPv2-MIB::sysLocation.0', 'Room 42')
...
```

The return value is a list of 2 elements *Tuples*, each containing:
- The *OID* in text format
- The *OID* value


##### Set

The `set` operation allows to set the value of a specific **writtable** *OID*.

```python
LOCATION_OID = ".1.3.6.1.2.1.1.6.0"

snmp = Snmp(host=HOST, port=PORT, community=RW_COMMUNITY, version=VERSION)
snmp.set(oid=LOCATION_OID, value="Room 200", datatype="str")
location = snmp.get(LOCATION_OID)

print(location)
("SNMPv2-MIB::sysLocation.0", "Room 200")
```

**Note:**

- The `Snmp` object must have been set up with a community with write permission on the remote host
- The `datatype` **must** be provided to the `Snmp.set()` method (see below for available *datatypes*)
- The `Snmp.set()` method does not return any value.

##### Available data types

| Datatype | *SNMP* equivalent | Info |
| --- | ---- | ------------- |
| `null` | `Null` | Null value |
| `bits` | `Bits` | The BITS construct represents an enumeration of named bits. This collection is assigned non-negative, contiguous values, starting at zero.   |
| `int` | `Integer32` | The Integer32 type represents integer-valued information between -2^31 and 2^31-1 inclusive |
| `str` | `OctetString` | The OCTET STRING type represents arbitrary binary or textual data. Size limit is variable. 255 octets allow max interoperability |
| `ipaddr` | `IpAddress` | The IpAddress type represents a 32-bit internet address. It is represented as an OCTET STRING of length 4, in network byte-order |
| `counter` | `Counter32` | The Counter32 type represents a non-negative integer which monotonically increases until it reaches a maximum value of 2^32 |
| `counter64` | `Counter64` | The Counter64 type represents a non-negative integer which monotonically increases until it reaches a maximum value of 2^64-1, when it wraps around and starts increasing again from zero |
| `gauge` | `Gauge32` | The Gauge32 type represents a non-negative integer, which may increase or decrease, but shall never exceed a maximum value, nor fall below a minimum value. The maximum value can not be greater than 2^32-1 |
| `unisgned` | `Unsigned32` | The Unsigned32 type represents integer-valued information between 0 and 2^32-1 inclusive (0 to 4294967295 decimal) |
| `ticks` | `TimeTicks` | The TimeTicks type represents a non-negative integer which represents the time, modulo 2^32 (4294967296 decimal), in hundredths of a second between two epochs. |
