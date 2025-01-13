import json
from pathlib import Path

_DOCKER_NOTIFY_PIPE = Path("/notify-pipe")


def _is_notification_enabled():
    # return _DOCKER_NOTIFY_PIPE.exists() and _DOCKER_NOTIFY_PIPE.is_fifo()
    return False


def _send_unraid_notification(subject: str, description: str, severity: str, message: str):
    if not _is_notification_enabled():
        return

    data = {
        'e': 'Cloudflare-DNS-Resolver',
        's': subject,
        'd': description,
        'i': severity,
        'm': message,
    }
    args = [f"-{key} {json.dumps(value)}" for key, value in data.items()]
    param = " ".join(args)

    with open(_DOCKER_NOTIFY_PIPE, "w") as fifo:
        fifo.write(param + "\n")


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
