# Cloudflare DNS Updater

Simple Python project to update a Cloudflare DNS automatically, mimicking Dynamic DNS.

Just execute `python run.py`.

## Unraid Usage

> Requires the **Compose Manager** and **User Scripts** plugin.

1. Create the Zone and the target Record as an A record (with Auto or any custom TTL).
2. Request a new API Key in Cloudflare with both Read and Write permissions to the Zone.
3. Create a new Compose Manager Stack.
4. Set up a new User Scripts script to launch the container every minute. 

### Compose Manager

```yml
name: cloudflare-dns

services:
  cloudflare-dns-resolver:
    container_name: cloudflare_resolver
    image: ghcr.io/barreeeiroo/cloudflare-dns-resolver:latest
    environment:
      CF_API_EMAIL: <YOUR_CLOUDFLARE_EMAIL_ADDRESS>
      CF_API_KEY: "${CF_API_KEY}"
      CF_ZONE_ID: "${CF_ZONE_ID}"
      CF_ZONE_RECORD: "<YOUR_CLOUDFLARE_ZONE_RECORD>"  # For example: "unraid.domain.org"
```

```env
CF_API_KEY=<YOUR_CLOUDFLARE_API_KEY>
CF_ZONE_ID=<YOUR_CLOUDFLARE_ZONE_API_ID>
```

### User Scripts

Run it on Custom Schedule at: `* * * * *` (every minute), for example.

```bash
#!/bin/bash
#backgroundOnly=true
#clearLog=true

docker container start cloudflare_resolver
```
