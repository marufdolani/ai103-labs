def test_facts_extracted(result):
    f = result["facts"]
    assert f["incident_id"] == "INC-4471"
    assert len(f["timeline"]) >= 5


def test_tool_step_computed_duration(result):
    assert result["outage_minutes"] == 45


def test_all_sections_present(result):
    for section in ["Summary", "Timeline", "Root cause", "Impact", "Action items"]:
        assert section.lower() in result["draft"].lower()


def test_verified(result):
    assert len(result["unsupported"]) <= 1
