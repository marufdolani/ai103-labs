def test_agent_card_discovered(result):
    assert result["card_name"] == "Contoso travel-policy agent"
    assert "travel-policy" in result["skills"]


def test_remote_agent_applies_policy(result):
    assert "economy" in result["direct"].lower()


def test_orchestrator_delegated(result):
    plan = result["plan"].lower()
    assert "business" in plan and "250" in plan
