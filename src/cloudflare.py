import os
from typing import Optional, Tuple
import requests

from utils import validate_ip

CF_API_KEY = os.getenv('CF_API_KEY')
CF_API_EMAIL = os.getenv('CF_API_EMAIL')

CF_ZONE_ID = os.getenv('CF_ZONE_ID')
CF_ZONE_RECORD = os.getenv('CF_ZONE_RECORD')


def _get_cloudflare_headers():
    return {
        "Authorization": f"Bearer {CF_API_KEY}",
        "Content-Type": "application/json",
        "X-Auth-Email": CF_API_EMAIL,
        # "X-Auth-Key": CF_API_KEY,
    }


def get_current_dns_ip() -> Optional[Tuple[str, str]]:
    try:
        params = {
            'name': CF_ZONE_RECORD,
            'proxied': False,
            'type': 'A',
        }

        response = requests.get(f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records",
                                headers=_get_cloudflare_headers(), params=params)
        response_json = response.json()
        if not response_json.get("success"):
            raise RuntimeError(f"Failed to call Cloudflare API: {response_json.get('errors')}")
        results = response_json.get("result", [])

        if len(results) != 1:
            print(f"Found {len(results)} results for {CF_ZONE_RECORD}; expected only 1")
            return None

        result = results[0]
        content = result.get("content")
        return validate_ip(content).exploded, result.get("id")

    except Exception as e:
        print(f"Failed to resolve current DNS: {e}")
        return None


def set_current_dns_ip(new_ip_address: str, record_id: str) -> bool:
    try:
        body = {
            'content': new_ip_address,
        }

        response = requests.patch(f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records/{record_id}",
                                  headers=_get_cloudflare_headers(), json=body)
        response_json = response.json()
        if not response_json.get("success"):
            raise RuntimeError(f"Failed to call Cloudflare API: {response_json.get('errors')}")
        return True

    except Exception as e:
        print(f"Failed to update current DNS: {e}")
        return False
