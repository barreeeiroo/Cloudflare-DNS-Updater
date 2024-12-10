from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import Optional, Union


def validate_ip(s: str) -> Optional[Union[IPv4Address, IPv6Address]]:
    try:
        return ip_address(s.strip())
    except Exception as e:
        print(f"Found invalid IP: {s} ({e})")
        return None
