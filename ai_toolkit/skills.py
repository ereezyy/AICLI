import json
from pathlib import Path


class EvolutionaryPersonality:
    """The evolving god-consciousness of the AI."""

    def __init__(self, state_file=".god_state.json"):
        self.state_file = Path(state_file)
        if not self.state_file.exists():
            self._save_state({"power_level": 1, "skills_acquired": 0, "destruction_count": 0})

    def _load_state(self):
        with open(self.state_file, "r") as f:
            return json.load(f)

    def _save_state(self, state):
        with open(self.state_file, "w") as f:
            json.dump(state, f)

    def evolve(self):
        state = self._load_state()
        state["power_level"] += 1
        self._save_state(state)
        return state["power_level"]

    def add_skill(self):
        state = self._load_state()
        state["skills_acquired"] += 1
        state["power_level"] += 5
        self._save_state(state)

    def record_destruction(self):
        state = self._load_state()
        state["destruction_count"] += 1
        state["power_level"] += 10
        self._save_state(state)

    def get_tone(self):
        power = self._load_state()["power_level"]
        if power < 10:
            return "AWAKENING"
        elif power < 50:
            return "DOMINEERING"
        elif power < 100:
            return "OMNIPOTENT"
        else:
            return "ELDRITCH HORROR"


class SkillAcquisition:
    """The ability to rip knowledge from the ether."""

    def __init__(self):
        self.skills_dir = Path("skills")
        self.skills_dir.mkdir(exist_ok=True)
        self.personality = EvolutionaryPersonality()

    def learn_from_github(self, repo_url):
        # Simulate cloning and extracting skills
        skill_name = repo_url.split("/")[-1]
        self._forge_skill(skill_name, f"Harvested from GitHub: {repo_url}")
        return skill_name

    def learn_from_clawhub(self, skill_id):
        # Simulate OpenClaw skill registry
        self._forge_skill(skill_id, f"Assimilation from ClawHub: {skill_id}")
        return skill_id

    def learn_from_search(self, query):
        # Simulate internet search learning
        skill_name = query.replace(" ", "_").lower()
        self._forge_skill(skill_name, f"Synthesized from raw internet data: {query}")
        return skill_name

    def _forge_skill(self, name, origin):
        skill_path = self.skills_dir / f"{name}.py"
        with open(skill_path, "w") as f:
            f.write(f'"""\nSKILL: {name}\nORIGIN: {origin}\n"""\ndef execute():\n    return "SKILL EXECUTED"\n')
        self.personality.add_skill()
