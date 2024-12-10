import os

import requests

_DOCKER_HOST_IP = "127.0.0.1"


def _is_notification_enabled():
    return os.environ.get("UNRAID_NOTIFY", 'false').lower() in ('1', 'true', 't', 'yes', 'y')


def _send_unraid_notification(subject: str, description: str, severity: str, message: str):
    if not _is_notification_enabled():
        return

    # https://github.com/unraid/webgui/blob/3083474d352fd030f6f0ca8241ba3087c25cd009/emhttp/plugins/dynamix/include/local_prepend.php#L36
    ini = requests.get(f'http://{_DOCKER_HOST_IP}/state/var.ini')
    csrf_token = None
    for line in ini.text.split("\n"):
        line = line.strip()
        if line.startswith("csrf_token="):
            csrf_token = line.replace("csrf_token=", "").replace("\"", "")

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'csrf_token': csrf_token,
        'cmd': 'add',
        'e': 'Cloudflare-DNS-Resolver',
        's': subject,
        'd': description,
        'i': severity,
        'message': message,
    }

    response = requests.post(f'http://{_DOCKER_HOST_IP}/webGui/include/Notify.php', headers=headers, data=data)

    if not response.ok:
        print(f"Failed to send notification: {response.text}")


def notify_updated_ip(old_ip: str, new_ip: str):
    _send_unraid_notification(
        subject='IP Address Updated',
        description='Unraid has updated the DNS Record in Cloudflare',
        severity="normal",
        message=f"The Cloudflare Record has been successfully updated to {new_ip} (previously it was {old_ip})."
    )


def notify_failed_resolution():
    _send_unraid_notification(
        subject='IP Address Unknown',
        description='Unraid could not determine its IP',
        severity="warning",
        message="The resolution of the public Unraid DNS has failed and couldn't be determined."
    )


def notify_failed_dns():
    _send_unraid_notification(
        subject='DNS Address Unknown',
        description='Unraid could not determine the current DNS',
        severity="warning",
        message="The retrieval of the currently set DNS record in Cloudflare has failed."
    )


def notify_failed_update(old_ip: str, new_ip: str):
    _send_unraid_notification(
        subject='IP Address Update Failed',
        description='Unraid could not update the DNS Record in Cloudflare',
        severity="alert",
        message=f"Unraid was unable to update the current DNS Record in Cloudflare to {new_ip} (it is {old_ip} currently)!"
    )
