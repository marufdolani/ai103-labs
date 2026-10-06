def test_round_trip_with_phrase_list(result):
    text = result["boosted"].lower()
    assert "contoso" in text and "november" in text


def test_diarization_finds_two_speakers(result):
    assert len(result["fast"]["speakers"]) == 2, result["fast"]["phrases"]
    assert "tokyo" in result["fast"]["text"].lower()


def test_speech_translation(result):
    tr = result["translation"]
    assert tr.get("fr") and tr.get("ja")
    assert "contoso" in tr["source"].lower()
