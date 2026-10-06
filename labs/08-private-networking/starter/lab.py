"""Lab 08 - Network-isolate the AI platform."""
import requests

from labkit import cfg, show
from labkit.clients import arm, arm_path, token


def main() -> dict:
    show.step("1. Isolation settings (ARM)")
    # TODO 1: GET the isolated Foundry resource; read publicNetworkAccess, networkAcls.defaultAction, PE connection states
    raise NotImplementedError("TODO 1: GET the isolated Foundry resource; read publicNetworkAccess, networkAcls.defaultAction, PE connection states  (see README step and solution/ if stuck)")
    show.kv({"publicNetworkAccess": public_access, "defaultAction": default_action, "private endpoints": pe_states})

    show.step("2. Private endpoint IP and DNS records")
    # TODO 2: GET the private endpoint; collect customDnsConfigs (fqdn -> ipAddresses)
    raise NotImplementedError("TODO 2: GET the private endpoint; collect customDnsConfigs (fqdn -> ipAddresses)  (see README step and solution/ if stuck)")
    for fqdn, ips in dns.items():
        print(f"   {fqdn} -> {', '.join(ips)}")

    show.step("3. Call from outside the VNet (valid token)")
    # TODO 3: POST a Language detection request to the isolated endpoint with a bearer token; keep the status code
    raise NotImplementedError("TODO 3: POST a Language detection request to the isolated endpoint with a bearer token; keep the status code  (see README step and solution/ if stuck)")
    show.warn(f"HTTP {public_status}: {r.text[:200]}")

    return {
        "public_network_access": public_access,
        "default_action": default_action,
        "pe_states": pe_states,
        "private_ips": sorted({ip for ips in dns.values() for ip in ips}),
        "public_call_status": public_status,
    }


if __name__ == "__main__":
    show.result(main())
