def test_token_audience_is_cognitive_services(result):
    assert "cognitiveservices.azure.com" in result["audience"]


def test_keyless_call_works(result):
    assert "keyless" in result["keyless_answer"].lower()


def test_key_auth_refused(result):
    assert result["key_status"] in (401, 403)


def test_local_auth_disabled(result):
    assert result["disable_local_auth"] is True
