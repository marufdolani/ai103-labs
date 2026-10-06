def test_openapi_tool_called(result):
    assert result["openapi_items"], f"no OpenAPI tool call found in {result['item_types']}"


def test_answer_uses_live_weather(result):
    answer = result["answer"].lower()
    assert "tokyo" in answer and ("°" in answer or "temperature" in answer or "rain" in answer)
