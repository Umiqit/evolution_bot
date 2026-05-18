import json
import os
import random
from typing import Dict, List, Optional, Tuple, Any

class SimulationStep:
    def __init__(self, stage_data: Dict = None):
        self.description = ""
        self.choices = []
        self.scientific_explanation = ""
        self.environment_changes = {}
        self.feedback_correct = ""
        self.feedback_incorrect = ""
        if stage_data:
            self.load_from_data(stage_data)
    
    def load_from_data(self, stage_data: Dict) -> None:
        self.description = stage_data.get("description", "")
        self.choices = stage_data.get("choices", [])
        self.scientific_explanation = stage_data.get("scientific_explanation", "")
        self.environment_changes = stage_data.get("environment_changes", {})
        self.feedback_correct = stage_data.get("feedback_correct", "")
        self.feedback_incorrect = stage_data.get("feedback_incorrect", "")
    
    def render(self) -> Tuple[str, List[str]]:
        text = self.description
        choice_texts = [choice.get("text", "") for choice in self.choices]
        return text, choice_texts
    
    def process_choice(self, choice_index: int) -> Dict:
        if choice_index < 0 or choice_index >= len(self.choices):
            return {
                "success": False,
                "error": "Неверный индекс выбора",
                "feedback": "Произошла ошибка. Пожалуйста, попробуйте снова."
            }
        
        choice = self.choices[choice_index]
        is_correct = choice.get("is_correct", False)
        effect = choice.get("effect", {})
        
        if is_correct:
            feedback = self.feedback_correct or "Правильный выбор!"
        else:
            feedback = self.feedback_incorrect or "Неправильный выбор."
        
        return {
            "success": True,
            "is_correct": is_correct,
            "effect": effect,
            "feedback": feedback,
            "scientific_explanation": self.scientific_explanation
        }

class Population:
    def __init__(self, initial_data: Dict = None):
        if initial_data is None:
            initial_data = {}
        
        genome_data = initial_data.get("genome_attributes", {})
        
        self.genome_attributes = {
            "colors": genome_data.get("colors", {"green": 850, "brown": 100, "spotted": 50}),
            "speed": genome_data.get("speed", 100),
            "camouflage": genome_data.get("camouflage", 50)
        }
        
        for key, value in genome_data.items():
            if key not in ["colors", "speed", "camouflage"]:
                self.genome_attributes[key] = value
        
        self.viability_index = initial_data.get("viability_index", 100)
        self.energy_reserve = initial_data.get("energy_reserve", 100)
        self.current_environment = initial_data.get("current_environment", {
            "type": "forest",
            "season": "autumn",
            "temperature": 15,
            "humidity": 60
        })
    
    def apply_effects(self, effects: Dict) -> None:
        if "colors" in effects:
            for color, change in effects["colors"].items():
                if color in self.genome_attributes["colors"]:
                    self.genome_attributes["colors"][color] = max(0, self.genome_attributes["colors"][color] + change)
        
        for key, value in effects.items():
            if key in ["green", "brown", "spotted", "sand", "dark", "silver", "blue", "striped", "bright", "camouflage_color"]:
                if "colors" in self.genome_attributes:
                    if key in self.genome_attributes["colors"]:
                        self.genome_attributes["colors"][key] = max(0, self.genome_attributes["colors"][key] + value)
                    else:
                        self.genome_attributes["colors"][key] = max(0, value)
            elif key in ["speed", "camouflage", "vigilance", "social", "aggression", "heat_tolerance", "cold_resistance", "water_storage", "burrowing", "climbing", "lung_capacity", "diet_diversity", "migration", "genetic_diversity", "nocturnal", "night_vision", "bioluminescence", "eye_size", "lateral_line", "agility", "caching", "memory", "territoriality", "stability", "speciation"]:
                current = self.genome_attributes.get(key, 0)
                self.genome_attributes[key] = max(0, current + value)
        
        viability_change = effects.get("viability_index", 0)
        if viability_change != 0:
            self.viability_index = max(0, min(100, self.viability_index + viability_change))
        
        energy_change = effects.get("energy_reserve", 0)
        if energy_change != 0:
            self.energy_reserve = max(0, min(200, self.energy_reserve + energy_change))
        
        self.calculate_viability()
    
    def calculate_viability(self) -> float:
        colors = self.genome_attributes.get("colors", {})
        if colors:
            total = sum(colors.values())
            if total > 0:
                diversity = 1 - (max(colors.values()) - min(colors.values())) / total if total > 0 else 0.5
            else:
                diversity = 0
        else:
            diversity = 0.5
        
        speed = self.genome_attributes.get("speed", 100) / 100
        camouflage = self.genome_attributes.get("camouflage", 50) / 100
        energy_factor = self.energy_reserve / 100
        
        env_factor = 1.0
        env_type = self.current_environment.get("type", "forest")
        season = self.current_environment.get("season", "autumn")
        
        if env_type == "forest":
            if season == "summer":
                env_factor = 1.1
            elif season == "winter":
                env_factor = 0.9
        
        self.viability_index = (
            diversity * 30 + speed * 25 + camouflage * 25 + energy_factor * 20
        ) * env_factor
        
        self.viability_index = max(0, min(100, self.viability_index))
        
        return self.viability_index
    
    def is_extinct(self) -> bool:
        colors = self.genome_attributes.get("colors", {})
        total_population = sum(colors.values())
        return self.viability_index <= 0 or self.energy_reserve <= 0 or total_population <= 0
    
    def update_environment(self, changes: Dict) -> None:
        for key, change in changes.items():
            if key in self.current_environment:
                if isinstance(self.current_environment[key], (int, float)):
                    self.current_environment[key] = max(0, self.current_environment.get(key, 0) + change)
    
    def reset(self) -> None:
        self.genome_attributes = {
            "colors": {"green": 850, "brown": 100, "spotted": 50},
            "speed": 100,
            "camouflage": 50
        }
        self.viability_index = 100
        self.energy_reserve = 100
        self.current_environment = {
            "type": "forest",
            "season": "autumn",
            "temperature": 15,
            "humidity": 60
        }
    
    def to_dict(self) -> Dict:
        return {
            "genome_attributes": self.genome_attributes,
            "viability_index": self.viability_index,
            "energy_reserve": self.energy_reserve,
            "current_environment": self.current_environment
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Population':
        return cls(data)
    
    def get_status(self) -> str:
        status = f"Жизнеспособность: {self.viability_index:.1f}%\n"
        status += f"Энергия: {self.energy_reserve:.1f}\n\n"
        status += "Генетические признаки:\n"
        
        colors = self.genome_attributes.get("colors", {})
        if colors:
            status += "  Окрасы:\n"
            for color, count in colors.items():
                status += f"    {color}: {count}\n"
        
        for attr in ["speed", "camouflage", "vigilance", "social", "heat_tolerance", "cold_resistance", "water_storage", "burrowing", "climbing", "lung_capacity", "diet_diversity", "genetic_diversity", "nocturnal"]:
            if attr in self.genome_attributes:
                status += f"  {attr}: {self.genome_attributes[attr]}\n"
        
        return status

class ScenarioGenerator:
    def __init__(self, content_path: str = 'data/content_bank.json'):
        self.content_path = content_path
        self.content = self.load_content()
        self.species_data = self.content.get("species", {})
    
    def load_content(self) -> Dict:
        try:
            if os.path.exists(self.content_path):
                with open(self.content_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                print(f"Файл {self.content_path} не найден")
                return {"scenarios": [], "species": {}}
        except Exception as e:
            print(f"Ошибка при загрузке контента: {e}")
            return {"scenarios": [], "species": {}}
    
    def get_random_scenario(self, completed_ids: List[str]) -> Optional[Dict]:
        scenarios = self.content.get("scenarios", [])
        available_scenarios = []
        
        for scenario in scenarios:
            if scenario.get("id") not in completed_ids:
                available_scenarios.append(scenario)
        
        if available_scenarios:
            return random.choice(available_scenarios)
        
        return None
    
    def get_scenario_by_id(self, scenario_id: str) -> Optional[Dict]:
        scenarios = self.content.get("scenarios", [])
        for scenario in scenarios:
            if scenario.get("id") == scenario_id:
                return scenario
        return None
    
    def get_stage_data(self, scenario_id: str, stage_index: int) -> Optional[Dict]:
        scenario = self.get_scenario_by_id(scenario_id)
        if scenario and "stages" in scenario and stage_index < len(scenario["stages"]):
            return scenario["stages"][stage_index]
        return None
    
    def check_species_reward(self, scenario_id: str, stage_index: int, population_data: Dict, result: Dict) -> Optional[str]:
        scenario = self.get_scenario_by_id(scenario_id)
        if not scenario:
            return None
        
        rare_species = scenario.get("rare_species", [])
        if not rare_species:
            return None
        
        if "rare_species" in result.get("effect", {}):
            return result["effect"]["rare_species"]
        
        if result.get("is_correct", False):
            viability = population_data.get("viability_index", 0)
            if viability > 90 and rare_species:
                return random.choice(rare_species)
            
            stages_count = len(scenario.get("stages", []))
            if stage_index == stages_count - 1:
                return random.choice(rare_species)
        
        return None
    
    def get_initial_population(self, scenario_id: str) -> Optional[Dict]:
        scenario = self.get_scenario_by_id(scenario_id)
        if scenario:
            return scenario.get("initial_population")
        return None
    
    def get_all_scenarios(self) -> List[Dict]:
        return self.content.get("scenarios", [])
    
    def get_scenario_count(self) -> int:
        return len(self.content.get("scenarios", []))
    
    def get_species_info(self, species_id: str) -> Optional[Dict]:
        return self.species_data.get(species_id)
    
    def get_all_species(self) -> Dict:
        return self.species_data
