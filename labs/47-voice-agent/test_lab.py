def test_transcript(result):
    t = result["transcript"].lower()
    assert "4471" in t.replace("-", "").replace(" ", "") or "b-4471" in t


def test_mood_from_audio(result):
    assert result["mood"] in {"frustrated", "sad"}, result["mood"]


def test_agent_acted(result):
    assert result["calls"] and result["booking"]["check_in"] == "2026-11-16"


def test_voice_reply_round_trip(result):
    heard = result["heard"].upper().replace(" ", "")
    assert "CF-2210" in heard or "CF2210" in heard


def test_japanese(result):
    assert "CF-2210" in result["japanese"]
