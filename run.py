from cloudflare import get_current_dns_ip, set_current_dns_ip
from resolver import resolve_ip


def main():
    ip_address = resolve_ip()
    current_dns, record_id = get_current_dns_ip()

    if not ip_address:
        print(f"Failed to find current IP address...")
        exit(1)
    if not current_dns:
        print(f"Failed to retrieve current DNS address...")
        exit(1)

    if ip_address == current_dns:
        print(f"IP Address in Cloudflare is in sync ({current_dns}), skipping...")
        return

    print(f"Trying to update IP from {current_dns} to {ip_address}...")
    if not set_current_dns_ip(new_ip_address=ip_address, record_id=record_id):
        exit(1)


if __name__ == "__main__":
    main()
