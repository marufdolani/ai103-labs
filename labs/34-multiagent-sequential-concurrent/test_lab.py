def test_sequential_runs_in_order(result):
    authors = [r["author"] for r in result["sequential"]]
    assert authors[-3:] == ["extractor", "drafter", "reviewer"], authors


def test_reviewer_decides(result):
    assert result["sequential"][-1]["text"].strip().upper().startswith(("APPROVED", "CHANGES"))


def test_concurrent_three_perspectives(result):
    assert {"legal", "finance", "privacy"} <= {r["author"] for r in result["concurrent"]}
