def test_single_turn(result):
    assert len(result["single"]) > 20


def test_streaming_arrives_in_chunks(result):
    assert result["stream_chunks"] > 1


def test_previous_response_id_keeps_state(result):
    assert "priya" in result["chained"].lower() and "sydney" in result["chained"].lower()


def test_conversation_keeps_state(result):
    assert "LT-5521" in result["conversation_answer"]
    assert result["conversation_items"] >= 4
