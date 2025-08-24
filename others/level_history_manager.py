import json
import os
from datetime import datetime

class LevelHistoryManager:
    def __init__(self, file_path = "history.json"):
        self.file_path = file_path
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        return {"teams": {}}

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=2)

    def record_attempt(self, team_name, level_name, time, points):
        team = self.data["teams"].setdefault(team_name, {"completed_levels": {}})
        level_attempts = team["completed_levels"].setdefault(level_name, [])
        level_attempts.append({
            "time": time,
            "points": points,
            "timestamp": datetime.now().isoformat()
        })
        self.save()

    def has_completed(self, team_name, level_name):
        return (
            team_name in self.data["teams"] and
            level_name in self.data["teams"][team_name]["completed_levels"]
        )

    def get_attempts(self, team_name, level_name):
        if self.has_completed(team_name, level_name):
            return self.data["teams"][team_name]["completed_levels"][level_name]
        return []
