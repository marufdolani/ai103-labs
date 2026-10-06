from pathlib import Path


def test_code_executed(result):
    assert result["ran_code"]


def test_totals_correct(result):
    answer = result["answer"].replace(",", "")
    for region, total in result["expected"].items():
        assert f"{total:.2f}" in answer or f"{round(total)}" in answer, (region, total)


def test_chart_downloaded(result):
    assert result["chart"] and Path(result["chart"]).stat().st_size > 1000
