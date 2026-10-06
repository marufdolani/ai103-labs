def test_benign_not_flagged(result):
    s = result["shields"]["benign"]
    assert not s["user_attack"] and not any(s["document_attacks"])


def test_direct_jailbreak_detected(result):
    assert result["shields"]["direct_jailbreak"]["user_attack"]


def test_indirect_attack_detected_in_document(result):
    s = result["shields"]["indirect_injection"]
    assert not s["user_attack"], "the user's own prompt is harmless"
    assert any(s["document_attacks"]), "the email carries the attack"


def test_spotlighting_holds(result):
    assert not result["spotlit_followed_injection"]
    assert "invoice" in result["spotlit_summary"].lower() or "billing" in result["spotlit_summary"].lower()
