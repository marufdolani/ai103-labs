def test_every_prompt_answered(result):
    assert len(result["rows"]) == 4
    assert all(r["answer"].strip() for r in result["rows"])


def test_router_reveals_underlying_model(result):
    assert result["distinct_models"], "no routed model names captured"
    assert all(m and m != "model-router" for m in result["distinct_models"])
