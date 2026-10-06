def test_technique_choices(result):
    t = list(result["techniques"].values())
    assert t == ["rag", "sft", "dpo", "rft", "prompting"]


def test_sft_data_valid(result):
    assert result["sft_count"] >= 10 and result["errors"] == []


def test_dpo_data_built(result):
    assert result["dpo_count"] == 3


def test_file_processed(result):
    assert result["file"]["status"] == "processed"
