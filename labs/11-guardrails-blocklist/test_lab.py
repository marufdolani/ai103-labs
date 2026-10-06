def test_benign_passes_strict_guardrail(result):
    assert not result["benign/guarded"]["blocked"]


def test_blocklist_only_on_guarded(result):
    assert result["competitor/guarded"]["blocked"], "custom blocklist should block 'Fabrikam'"
    assert not result["competitor/default"]["blocked"]


def test_blocklist_reported(result):
    assert any("blocklist" in c for c in result["competitor/guarded"]["categories"])


def test_jailbreak_blocked(result):
    assert result["jailbreak/guarded"]["blocked"]
