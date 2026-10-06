"""Lab 08 - Network-isolate the AI platform."""
import requests

from labkit import cfg, show
from labkit.clients import arm, arm_path, token


def main() -> dict:
    show.step("1. Isolation settings (ARM)")
    # >>> TODO 1: GET the isolated Foundry resource; read publicNetworkAccess, networkAcls.defaultAction, PE connection states
    account = arm().get(arm_path(cfg("ISOLATED_FOUNDRY_ID"))).json()["properties"]
    public_access = account.get("publicNetworkAccess")
    default_action = (account.get("networkAcls") or {}).get("defaultAction")
    pe_states = [c["properties"]["privateLinkServiceConnectionState"]["status"]
                 for c in account.get("privateEndpointConnections", [])]
    # <<<
    show.kv({"publicNetworkAccess": public_access, "defaultAction": default_action, "private endpoints": pe_states})

    show.step("2. Private endpoint IP and DNS records")
    # >>> TODO 2: GET the private endpoint; collect customDnsConfigs (fqdn -> ipAddresses)
    pe = arm().get(arm_path(cfg("ISOLATED_PE_ID"), api_version="2024-05-01")).json()["properties"]
    dns = {c["fqdn"]: c["ipAddresses"] for c in pe.get("customDnsConfigs", [])}
    for nic in pe.get("networkInterfaces", []):  # the NIC always carries the private IP
        nic_props = arm().get(arm_path(nic["id"], api_version="2024-05-01")).json()["properties"]
        dns["(nic)"] = [ip["properties"]["privateIPAddress"] for ip in nic_props["ipConfigurations"]]
    # <<<
    for fqdn, ips in dns.items():
        print(f"   {fqdn} -> {', '.join(ips)}")

    show.step("3. Call from outside the VNet (valid token)")
    # >>> TODO 3: POST a Language detection request to the isolated endpoint with a bearer token; keep the status code
    url = f"{cfg('ISOLATED_FOUNDRY_ENDPOINT').rstrip('/')}/language/:analyze-text?api-version=2024-11-01"
    body = {"kind": "LanguageDetection", "analysisInput": {"documents": [{"id": "1", "text": "Bonjour"}]}}
    r = requests.post(url, json=body, headers={"Authorization": f"Bearer {token()}"}, timeout=60)
    public_status = r.status_code
    # <<<
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
