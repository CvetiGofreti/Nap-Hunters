import json
from pathlib import Path
from others.level_history_manager import LevelHistoryManager

def test_empty_file(tmp_path: Path):
    manager = LevelHistoryManager(tmp_path / "history.json")
    assert manager.data == {"teams": {}}
    assert not (tmp_path / "history.json").exists()

def test_record_attempt(tmp_path: Path):
    file_path = tmp_path / "history.json"
    manager = LevelHistoryManager(file_path)
    manager.record_attempt("TeamA", "Level1", time = 12.3, points = 100)
    assert "TeamA" in manager.data["teams"]
    assert "Level1" in manager.data["teams"]["TeamA"]["completed_levels"]
    saved = json.loads(file_path.read_text(encoding="utf-8"))
    entry = saved["teams"]["TeamA"]["completed_levels"]["Level1"][0]
    assert entry["time"] == 12.3
    assert entry["points"] == 100

def test_completed_level(tmp_path: Path):
    manager = LevelHistoryManager(tmp_path / "history.json")
    assert not manager.has_completed("team", "level")
    manager.record_attempt("team", "level", time = 1.0, points = 1)
    assert manager.has_completed("team", "level")
    assert not manager.has_completed("team", "level2")
