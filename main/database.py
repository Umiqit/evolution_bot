# database.ipynb

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

class DataStorage:
    def __init__(self, file_path: str = '../data/users.json'):
        self.file_path = file_path
        self.data = self.load_data()
    
    def load_data(self) -> Dict:
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                return {"users": {}}
        except:
            return {"users": {}}
    
    def save_data(self) -> bool:
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def get_user(self, user_id: int) -> Dict:
        user_id_str = str(user_id)
        if user_id_str not in self.data["users"]:
            self.data["users"][user_id_str] = {
                "user_id": user_id,
                "username": "",
                "first_name": "",
                "progress_level": 1,
                "experience": 0,
                "status_level": "Наблюдатель",
                "state": "main_menu",
                "current_scenario_id": None,
                "current_stage": 0,
                "current_population": None,
                "collected_species": [],
                "completed_scenarios": [],
                "achievements_unlocked": [],
                "created_at": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat()
            }
            self.save_data()
        return self.data["users"][user_id_str]
    
    def update_user(self, user_id: int, new_data: Dict) -> bool:
        user_id_str = str(user_id)
        if user_id_str in self.data["users"]:
            new_data["last_active"] = datetime.now().isoformat()
            self.data["users"][user_id_str].update(new_data)
            return self.save_data()
        return False
    
    def get_all_users(self) -> Dict:
        return self.data["users"]


class User:
    STATUS_LEVELS = {
        "Наблюдатель": 0,
        "Адаптатор": 100,
        "Архитектор биосферы": 300,
        "Творец эволюции": 600
    }
    
    def __init__(self, user_id: int, username: str = "", first_name: str = ""):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.progress_level = 1
        self.experience = 0
        self.status_level = "Наблюдатель"
        self.state = "main_menu"
        self.current_scenario_id = None
        self.current_stage = 0
        self.current_population = None
        self.collected_species = []
        self.completed_scenarios = []
        self.achievements_unlocked = []
    
    def start_new_simulation(self, scenario_id: str, initial_population_data: dict) -> None:
        self.current_scenario_id = scenario_id
        self.current_stage = 0
        self.current_population = initial_population_data
        self.state = "simulation_active"
    
    def finish_simulation(self) -> None:
        if self.current_scenario_id and self.current_scenario_id not in self.completed_scenarios:
            self.completed_scenarios.append(self.current_scenario_id)
        self.current_scenario_id = None
        self.current_stage = 0
        self.current_population = None
        self.state = "main_menu"
    
    def update_progress(self, value: int) -> None:
        self.experience += value
        new_level = (self.experience // 50) + 1
        if new_level > self.progress_level:
            self.progress_level = new_level
        for rank, required_exp in self.STATUS_LEVELS.items():
            if self.experience >= required_exp:
                self.status_level = rank
        if self.experience >= 1000:
            self.status_level = "Творец эволюции"
    
    def add_species(self, species_id: str) -> None:
        if species_id not in self.collected_species:
            self.collected_species.append(species_id)
    
    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "first_name": self.first_name,
            "progress_level": self.progress_level,
            "experience": self.experience,
            "status_level": self.status_level,
            "state": self.state,
            "current_scenario_id": self.current_scenario_id,
            "current_stage": self.current_stage,
            "current_population": self.current_population,
            "collected_species": self.collected_species,
            "completed_scenarios": self.completed_scenarios,
            "achievements_unlocked": self.achievements_unlocked
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        user = cls(
            user_id=data.get("user_id", 0),
            username=data.get("username", ""),
            first_name=data.get("first_name", "")
        )
        user.progress_level = data.get("progress_level", 1)
        user.experience = data.get("experience", 0)
        user.status_level = data.get("status_level", "Наблюдатель")
        user.state = data.get("state", "main_menu")
        user.current_scenario_id = data.get("current_scenario_id")
        user.current_stage = data.get("current_stage", 0)
        user.current_population = data.get("current_population")
        user.collected_species = data.get("collected_species", [])
        user.completed_scenarios = data.get("completed_scenarios", [])
        user.achievements_unlocked = data.get("achievements_unlocked", [])
        return user


class AchievementSystem:
    ACHIEVEMENTS = {
        "first_step": {
            "name": "Первый шаг",
            "description": "Начать первую эволюцию",
            "condition": lambda user: len(user.completed_scenarios) >= 1
        },
        "collector_1": {
            "name": "Коллекционер I",
            "description": "Собрать 3 вида",
            "condition": lambda user: len(user.collected_species) >= 3
        },
        "collector_2": {
            "name": "Коллекционер II",
            "description": "Собрать 10 видов",
            "condition": lambda user: len(user.collected_species) >= 10
        },
        "explorer_1": {
            "name": "Исследователь I",
            "description": "Пройдите 5 сценариев",
            "condition": lambda user: len(user.completed_scenarios) >= 5
        },
        "explorer_2": {
            "name": "Исследователь II",
            "description": "Пройдите все сценарии",
            "condition": lambda user: len(user.completed_scenarios) >= 10
        },
        "survivor": {
            "name": "Выживший",
            "description": "Выжить в сложных условиях",
            "condition": lambda user: user.progress_level >= 10
        }
    }
    
    @classmethod
    def check_achievements(cls, user: User) -> List[str]:
        new_achievements = []
        for ach_id, ach_data in cls.ACHIEVEMENTS.items():
            if ach_id not in user.achievements_unlocked:
                if ach_data["condition"](user):
                    user.achievements_unlocked.append(ach_id)
                    new_achievements.append(ach_data["name"])
        return new_achievements
__all__ = ['DataStorage', 'User', 'AchievementSystem']
