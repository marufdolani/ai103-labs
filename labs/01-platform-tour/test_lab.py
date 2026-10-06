from labkit import cfg


def test_core_deployments_exist(result):
    for name in (cfg("CHAT_MODEL"), cfg("LARGE_MODEL"), cfg("EMBEDDING_MODEL")):
        assert name in result["deployments"], f"deployment {name} not found"


def test_search_connection(result):
    assert any("search" in t for t in result["connection_types"]), result["connection_types"]


def test_appinsights_connected(result):
    assert result["appinsights_connected"]


def test_model_answered(result):
    assert len(result["answer"].strip()) > 10
