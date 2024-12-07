from typing import Optional, List, Callable

import requests

from utils import validate_ip


def _resolve_with_icanhazip():
    try:
        response = requests.get("https://ipv4.icanhazip.com/")
        return response.text
    except Exception as e:
        print(f"Failed to resolve with icanhazip: {e}")
        return None


def _resolve_with_ipify():
    try:
        response = requests.get("https://api.ipify.org/")
        return response.text
    except Exception as e:
        print(f"Failed to resolve with ipify: {e}")
        return None


def _resolve_with_cloudflare():
    try:
        response = requests.get("https://cloudflare.com/cdn-cgi/trace")
        lines = response.text.split("\n")
        response_map = {line.split("=")[0]: line.split("=")[1] for line in lines if "=" in line}
        return response_map.get("ip")
    except Exception as e:
        print(f"Failed to resolve with cloudflare: {e}")
        return None


def resolve_ip() -> Optional[str]:
    resolvers: List[Callable[[], Optional[str]]] = [
        _resolve_with_icanhazip,
        _resolve_with_ipify,
        _resolve_with_cloudflare,
    ]

    for resolver in resolvers:
        candidate_str = resolver()

        if candidate_str:
            candidate_ip = validate_ip(candidate_str)
            if not candidate_ip:
                print(f"Failed to validate IP for {resolver}")
                continue

            return candidate_ip.exploded

    return None
