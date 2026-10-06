def test_public_access_disabled(result):
    assert result["public_network_access"] == "Disabled"
    assert result["default_action"] == "Deny"


def test_private_endpoint_approved(result):
    assert "Approved" in result["pe_states"]


def test_private_ip_in_vnet(result):
    assert any(ip.startswith("10.80.") for ip in result["private_ips"])


def test_internet_call_blocked(result):
    assert result["public_call_status"] == 403
