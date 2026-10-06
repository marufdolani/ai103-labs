from pathlib import Path


def test_all_jobs_completed(result):
    assert result["statuses"] == ["completed", "completed", "completed"], result["statuses"]


def test_videos_downloaded(result):
    assert all(p and Path(p).stat().st_size > 50_000 for p in result["files"])
