import json
from datetime import datetime
import os

class LevelHistoryManager:
    def __init__(self, file_path="history.json"):
        self.file_path = file_path
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return {"teams": {}}

    def save(self):
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=2)

    def record_attempt(self, teamName, levelName, time, points):
        team = self.data["teams"].setdefault(teamName, {"completed_levels": {}})
        levelAttempts = team["completed_levels"].setdefault(levelName, [])
        levelAttempts.append({
            "time": time,
            "points": points,
            "timestamp": datetime.now().isoformat()
        })
        self.save()

    def has_completed(self, teamName, levelName):
        return (
            teamName in self.data["teams"] and
            levelName in self.data["teams"][teamName]["completed_levels"]
        )

    def get_attempts(self, teamName, levelName):
        if self.has_completed(teamName, levelName):
            return self.data["teams"][teamName]["completed_levels"][levelName]
        return []