def test_developer_gets_foundry_user(result):
    assert result["picks"]["developer"] == "Foundry User"


def test_admin_gets_account_owner(result):
    assert result["picks"]["platform_admin"] == "Foundry Account Owner"


def test_lead_gets_project_manager(result):
    assert result["picks"]["team_lead"] == "Foundry Project Manager"


def test_account_owner_cannot_build(result):
    assert result["matrix"]["Foundry Account Owner"]["build_agents"] is False


def test_platform_granted_you_foundry_user(result):
    assert "53ca6127-db72-4b80-b1b0-d745d6d5456d" in result["assigned_role_ids"]
