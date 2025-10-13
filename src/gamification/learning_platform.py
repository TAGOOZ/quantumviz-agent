#!/usr/bin/env python3
"""
QuantumViz Agent - Gamified Learning Platform
Interactive quantum learning with challenges, leaderboards, and community features.
"""

import json
import time
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib

class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class ChallengeType(Enum):
    CIRCUIT_BUILDING = "circuit_building"
    CONCEPT_QUIZ = "concept_quiz"
    ALGORITHM_IMPLEMENTATION = "algorithm_implementation"
    OPTIMIZATION = "optimization"
    DEBUGGING = "debugging"

@dataclass
class User:
    user_id: str
    username: str
    level: DifficultyLevel
    xp: int
    badges: List[str]
    achievements: List[str]
    circuits_created: int
    challenges_completed: int
    join_date: str

@dataclass
class Challenge:
    challenge_id: str
    title: str
    description: str
    challenge_type: ChallengeType
    difficulty: DifficultyLevel
    xp_reward: int
    badge_reward: Optional[str]
    requirements: Dict[str, Any]
    solution: Dict[str, Any]
    hints: List[str]

@dataclass
class LeaderboardEntry:
    rank: int
    user: User
    score: int
    xp: int
    badges_count: int

class QuantumLearningPlatform:
    """Gamified quantum learning platform with challenges and community features."""
    
    def __init__(self):
        self.users = {}
        self.challenges = {}
        self.leaderboards = {}
        self.circuit_gallery = {}
        self.achievements = self._initialize_achievements()
        self.badges = self._initialize_badges()
        self._create_sample_challenges()
        
    def _initialize_achievements(self) -> Dict[str, Dict[str, Any]]:
        """Initialize achievement system."""
        return {
            "first_circuit": {
                "name": "First Steps",
                "description": "Create your first quantum circuit",
                "icon": "🎯",
                "xp_reward": 50
            },
            "bell_state_master": {
                "name": "Bell State Master",
                "description": "Successfully create a Bell state",
                "icon": "🔗",
                "xp_reward": 100
            },
            "grover_expert": {
                "name": "Grover's Algorithm Expert",
                "description": "Implement Grover's search algorithm",
                "icon": "🔍",
                "xp_reward": 200
            },
            "shor_implementer": {
                "name": "Shor's Algorithm Implementer",
                "description": "Implement Shor's factorization algorithm",
                "icon": "🔢",
                "xp_reward": 300
            },
            "circuit_optimizer": {
                "name": "Circuit Optimizer",
                "description": "Optimize a circuit to reduce gate count",
                "icon": "⚡",
                "xp_reward": 150
            },
            "quantum_teacher": {
                "name": "Quantum Teacher",
                "description": "Help 10 other users with their circuits",
                "icon": "👨‍🏫",
                "xp_reward": 250
            },
            "hardware_runner": {
                "name": "Hardware Runner",
                "description": "Run a circuit on real quantum hardware",
                "icon": "🚀",
                "xp_reward": 500
            }
        }
    
    def _initialize_badges(self) -> Dict[str, Dict[str, Any]]:
        """Initialize badge system."""
        return {
            "quantum_novice": {
                "name": "Quantum Novice",
                "description": "Complete 5 beginner challenges",
                "icon": "🌱",
                "color": "green"
            },
            "entanglement_explorer": {
                "name": "Entanglement Explorer",
                "description": "Master entanglement concepts",
                "icon": "🔗",
                "color": "blue"
            },
            "algorithm_master": {
                "name": "Algorithm Master",
                "description": "Implement 3 quantum algorithms",
                "icon": "🧠",
                "color": "purple"
            },
            "optimization_guru": {
                "name": "Optimization Guru",
                "description": "Optimize 5 circuits",
                "icon": "⚡",
                "color": "orange"
            },
            "hardware_pioneer": {
                "name": "Hardware Pioneer",
                "description": "Run circuits on real quantum hardware",
                "icon": "🚀",
                "color": "red"
            }
        }
    
    def _create_sample_challenges(self):
        """Create sample challenges for the platform."""
        challenges = [
            Challenge(
                challenge_id="bell_state_creation",
                title="Create Your First Bell State",
                description="Build a quantum circuit that creates a Bell state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2",
                challenge_type=ChallengeType.CIRCUIT_BUILDING,
                difficulty=DifficultyLevel.BEGINNER,
                xp_reward=100,
                badge_reward="quantum_novice",
                requirements={
                    "gates": ["H", "CNOT"],
                    "qubits": 2,
                    "max_gates": 3
                },
                solution={
                    "gates": [
                        {"type": "H", "qubit": 0},
                        {"type": "CNOT", "qubit": 0, "target": 1}
                    ]
                },
                hints=[
                    "Start with a Hadamard gate on the first qubit",
                    "Use CNOT to entangle the qubits",
                    "Remember: H creates superposition, CNOT creates entanglement"
                ]
            ),
            Challenge(
                challenge_id="grover_search_implementation",
                title="Implement Grover's Search",
                description="Build a Grover search circuit to find marked items in a database",
                challenge_type=ChallengeType.ALGORITHM_IMPLEMENTATION,
                difficulty=DifficultyLevel.ADVANCED,
                xp_reward=300,
                badge_reward="algorithm_master",
                requirements={
                    "algorithm": "grover",
                    "search_space": 4,
                    "target_items": [2, 3]
                },
                solution={
                    "gates": [
                        {"type": "H", "qubit": 0},
                        {"type": "H", "qubit": 1},
                        {"type": "X", "qubit": 0},
                        {"type": "CZ", "qubit": 0, "target": 1},
                        {"type": "X", "qubit": 0},
                        {"type": "H", "qubit": 0},
                        {"type": "H", "qubit": 1}
                    ]
                },
                hints=[
                    "Initialize all qubits in superposition",
                    "Apply the oracle to mark target states",
                    "Use the diffusion operator to amplify marked states"
                ]
            ),
            Challenge(
                challenge_id="circuit_optimization",
                title="Optimize This Circuit",
                description="Reduce the gate count of this circuit while maintaining the same functionality",
                challenge_type=ChallengeType.OPTIMIZATION,
                difficulty=DifficultyLevel.INTERMEDIATE,
                xp_reward=150,
                badge_reward="optimization_guru",
                requirements={
                    "original_gates": 6,
                    "target_gates": 3,
                    "functionality": "must_remain_same"
                },
                solution={
                    "optimized_gates": [
                        {"type": "H", "qubit": 0},
                        {"type": "CNOT", "qubit": 0, "target": 1}
                    ]
                },
                hints=[
                    "Look for consecutive identical gates",
                    "Remember that H-H = I (identity)",
                    "X-X = I, so consecutive X gates can be removed"
                ]
            ),
            Challenge(
                challenge_id="quantum_teleportation",
                title="Quantum Teleportation Protocol",
                description="Implement the quantum teleportation protocol to transfer a qubit state",
                challenge_type=ChallengeType.CIRCUIT_BUILDING,
                difficulty=DifficultyLevel.ADVANCED,
                xp_reward=250,
                badge_reward="entanglement_explorer",
                requirements={
                    "qubits": 3,
                    "protocol": "teleportation",
                    "measurements": 2
                },
                solution={
                    "gates": [
                        {"type": "H", "qubit": 0},
                        {"type": "CNOT", "qubit": 0, "target": 1},
                        {"type": "CNOT", "qubit": 2, "target": 0},
                        {"type": "H", "qubit": 2},
                        {"type": "measure", "qubit": 0},
                        {"type": "measure", "qubit": 2}
                    ]
                },
                hints=[
                    "Alice and Bob need to share an entangled state",
                    "Alice performs measurements on her qubits",
                    "Bob applies corrections based on Alice's results"
                ]
            )
        ]
        
        for challenge in challenges:
            self.challenges[challenge.challenge_id] = challenge
    
    def register_user(self, username: str, level: DifficultyLevel = DifficultyLevel.BEGINNER) -> User:
        """Register a new user."""
        user_id = hashlib.md5(f"{username}{time.time()}".encode()).hexdigest()[:8]
        
        user = User(
            user_id=user_id,
            username=username,
            level=level,
            xp=0,
            badges=[],
            achievements=[],
            circuits_created=0,
            challenges_completed=0,
            join_date=time.strftime("%Y-%m-%d")
        )
        
        self.users[user_id] = user
        return user
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile with stats."""
        if user_id not in self.users:
            return None
        
        user = self.users[user_id]
        return {
            "user": asdict(user),
            "level_progress": self._calculate_level_progress(user),
            "recent_achievements": self._get_recent_achievements(user),
            "next_badges": self._get_next_badges(user)
        }
    
    def submit_challenge_solution(self, user_id: str, challenge_id: str, solution: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a solution to a challenge."""
        if user_id not in self.users or challenge_id not in self.challenges:
            return {"success": False, "error": "Invalid user or challenge"}
        
        user = self.users[user_id]
        challenge = self.challenges[challenge_id]
        
        # Check if user meets difficulty requirements
        if self._get_difficulty_level(user.xp) < challenge.difficulty:
            return {
                "success": False,
                "error": f"Challenge requires {challenge.difficulty.value} level or higher"
            }
        
        # Validate solution
        is_correct = self._validate_solution(challenge, solution)
        
        if is_correct:
            # Award XP and badges
            user.xp += challenge.xp_reward
            user.challenges_completed += 1
            
            if challenge.badge_reward and challenge.badge_reward not in user.badges:
                user.badges.append(challenge.badge_reward)
            
            # Check for new achievements
            new_achievements = self._check_achievements(user)
            user.achievements.extend(new_achievements)
            
            return {
                "success": True,
                "xp_gained": challenge.xp_reward,
                "badges_earned": [challenge.badge_reward] if challenge.badge_reward else [],
                "achievements": new_achievements,
                "level_up": self._check_level_up(user)
            }
        else:
            return {
                "success": False,
                "error": "Solution is incorrect",
                "hints": challenge.hints
            }
    
    def create_circuit_gallery_entry(self, user_id: str, circuit: Dict[str, Any], 
                                   title: str, description: str) -> str:
        """Add a circuit to the community gallery."""
        if user_id not in self.users:
            return None
        
        entry_id = hashlib.md5(f"{user_id}{time.time()}".encode()).hexdigest()[:8]
        
        entry = {
            "entry_id": entry_id,
            "user_id": user_id,
            "username": self.users[user_id].username,
            "title": title,
            "description": description,
            "circuit": circuit,
            "likes": 0,
            "forks": 0,
            "created_date": time.strftime("%Y-%m-%d"),
            "tags": self._extract_circuit_tags(circuit)
        }
        
        self.circuit_gallery[entry_id] = entry
        self.users[user_id].circuits_created += 1
        
        return entry_id
    
    def get_circuit_gallery(self, limit: int = 20, sort_by: str = "recent") -> List[Dict[str, Any]]:
        """Get circuits from the community gallery."""
        entries = list(self.circuit_gallery.values())
        
        if sort_by == "recent":
            entries.sort(key=lambda x: x["created_date"], reverse=True)
        elif sort_by == "popular":
            entries.sort(key=lambda x: x["likes"], reverse=True)
        elif sort_by == "forks":
            entries.sort(key=lambda x: x["forks"], reverse=True)
        
        return entries[:limit]
    
    def get_leaderboard(self, category: str = "xp", limit: int = 10) -> List[LeaderboardEntry]:
        """Get leaderboard for specified category."""
        users = list(self.users.values())
        
        if category == "xp":
            users.sort(key=lambda x: x.xp, reverse=True)
        elif category == "challenges":
            users.sort(key=lambda x: x.challenges_completed, reverse=True)
        elif category == "circuits":
            users.sort(key=lambda x: x.circuits_created, reverse=True)
        elif category == "badges":
            users.sort(key=lambda x: len(x.badges), reverse=True)
        
        leaderboard = []
        for i, user in enumerate(users[:limit]):
            score = user.xp if category == "xp" else getattr(user, category, 0)
            leaderboard.append(LeaderboardEntry(
                rank=i + 1,
                user=user,
                score=score,
                xp=user.xp,
                badges_count=len(user.badges)
            ))
        
        return leaderboard
    
    def _calculate_level_progress(self, user: User) -> Dict[str, Any]:
        """Calculate user's level progress."""
        current_level = self._get_difficulty_level(user.xp)
        xp_for_current_level = self._get_xp_for_level(current_level)
        xp_for_next_level = self._get_xp_for_level(self._get_next_level(current_level))
        
        progress = (user.xp - xp_for_current_level) / (xp_for_next_level - xp_for_current_level)
        
        return {
            "current_level": current_level.value,
            "xp": user.xp,
            "xp_for_current": xp_for_current_level,
            "xp_for_next": xp_for_next_level,
            "progress_percentage": progress * 100
        }
    
    def _get_difficulty_level(self, xp: int) -> DifficultyLevel:
        """Get difficulty level based on XP."""
        if xp < 100:
            return DifficultyLevel.BEGINNER
        elif xp < 500:
            return DifficultyLevel.INTERMEDIATE
        elif xp < 1000:
            return DifficultyLevel.ADVANCED
        else:
            return DifficultyLevel.EXPERT
    
    def _get_next_level(self, current_level: DifficultyLevel) -> DifficultyLevel:
        """Get next difficulty level."""
        levels = [DifficultyLevel.BEGINNER, DifficultyLevel.INTERMEDIATE, 
                 DifficultyLevel.ADVANCED, DifficultyLevel.EXPERT]
        current_index = levels.index(current_level)
        return levels[min(current_index + 1, len(levels) - 1)]
    
    def _get_xp_for_level(self, level: DifficultyLevel) -> int:
        """Get XP required for a level."""
        xp_requirements = {
            DifficultyLevel.BEGINNER: 0,
            DifficultyLevel.INTERMEDIATE: 100,
            DifficultyLevel.ADVANCED: 500,
            DifficultyLevel.EXPERT: 1000
        }
        return xp_requirements[level]
    
    def _validate_solution(self, challenge: Challenge, solution: Dict[str, Any]) -> bool:
        """Validate a challenge solution."""
        # Simplified validation - in real implementation, this would be more sophisticated
        if challenge.challenge_type == ChallengeType.CIRCUIT_BUILDING:
            return self._validate_circuit_solution(challenge, solution)
        elif challenge.challenge_type == ChallengeType.CONCEPT_QUIZ:
            return self._validate_quiz_solution(challenge, solution)
        else:
            return True  # Placeholder for other challenge types
    
    def _validate_circuit_solution(self, challenge: Challenge, solution: Dict[str, Any]) -> bool:
        """Validate circuit building solution."""
        # Check if solution matches requirements
        gates = solution.get("gates", [])
        requirements = challenge.requirements
        
        # Check gate types
        required_gates = requirements.get("gates", [])
        solution_gates = [gate.get("type") for gate in gates]
        
        for req_gate in required_gates:
            if req_gate not in solution_gates:
                return False
        
        # Check qubit count
        max_qubits = requirements.get("qubits", 0)
        used_qubits = set()
        for gate in gates:
            used_qubits.add(gate.get("qubit", 0))
            if gate.get("target") is not None:
                used_qubits.add(gate.get("target"))
        
        if len(used_qubits) > max_qubits:
            return False
        
        return True
    
    def _validate_quiz_solution(self, challenge: Challenge, solution: Dict[str, Any]) -> bool:
        """Validate quiz solution."""
        # Simplified quiz validation
        return solution.get("correct", False)
    
    def _check_achievements(self, user: User) -> List[str]:
        """Check for new achievements."""
        new_achievements = []
        
        # First circuit achievement
        if user.circuits_created >= 1 and "first_circuit" not in user.achievements:
            new_achievements.append("first_circuit")
        
        # Challenge completion achievements
        if user.challenges_completed >= 5 and "challenge_master" not in user.achievements:
            new_achievements.append("challenge_master")
        
        # XP-based achievements
        if user.xp >= 1000 and "xp_master" not in user.achievements:
            new_achievements.append("xp_master")
        
        return new_achievements
    
    def _check_level_up(self, user: User) -> bool:
        """Check if user leveled up."""
        old_level = self._get_difficulty_level(user.xp - 100)  # Assuming they just gained 100 XP
        new_level = self._get_difficulty_level(user.xp)
        return old_level != new_level
    
    def _get_recent_achievements(self, user: User) -> List[Dict[str, Any]]:
        """Get recent achievements for user."""
        recent = []
        for achievement_id in user.achievements[-3:]:  # Last 3 achievements
            if achievement_id in self.achievements:
                achievement = self.achievements[achievement_id]
                recent.append({
                    "id": achievement_id,
                    "name": achievement["name"],
                    "description": achievement["description"],
                    "icon": achievement["icon"]
                })
        return recent
    
    def _get_next_badges(self, user: User) -> List[Dict[str, Any]]:
        """Get next badges user can earn."""
        next_badges = []
        for badge_id, badge in self.badges.items():
            if badge_id not in user.badges:
                next_badges.append({
                    "id": badge_id,
                    "name": badge["name"],
                    "description": badge["description"],
                    "icon": badge["icon"]
                })
        return next_badges[:3]  # Show next 3 badges
    
    def _extract_circuit_tags(self, circuit: Dict[str, Any]) -> List[str]:
        """Extract tags from circuit for categorization."""
        tags = []
        gates = circuit.get("gates", [])
        
        gate_types = [gate.get("type") for gate in gates]
        
        if "H" in gate_types:
            tags.append("superposition")
        if "CNOT" in gate_types or "CZ" in gate_types:
            tags.append("entanglement")
        if "measure" in gate_types or "M" in gate_types:
            tags.append("measurement")
        
        return tags

# Demo function
def demo_gamified_learning():
    """Demonstrate gamified learning platform."""
    print("🎮 QuantumViz Agent - Gamified Learning Platform Demo")
    print("=" * 60)
    
    # Initialize platform
    platform = QuantumLearningPlatform()
    
    # Register users
    alice = platform.register_user("Alice", DifficultyLevel.BEGINNER)
    bob = platform.register_user("Bob", DifficultyLevel.INTERMEDIATE)
    charlie = platform.register_user("Charlie", DifficultyLevel.ADVANCED)
    
    print(f"👥 Users Registered: {len(platform.users)}")
    print(f"🎯 Challenges Available: {len(platform.challenges)}")
    print(f"🏆 Achievements: {len(platform.achievements)}")
    print(f"🎖️ Badges: {len(platform.badges)}")
    
    # Demo challenge submission
    print(f"\n🧪 Alice attempts Bell State Challenge:")
    bell_solution = {
        "gates": [
            {"type": "H", "qubit": 0},
            {"type": "CNOT", "qubit": 0, "target": 1}
        ]
    }
    
    result = platform.submit_challenge_solution(
        alice.user_id, "bell_state_creation", bell_solution
    )
    
    if result["success"]:
        print(f"✅ Challenge completed!")
        print(f"   XP Gained: {result['xp_gained']}")
        print(f"   Badges: {result['badges_earned']}")
        print(f"   Achievements: {result['achievements']}")
    else:
        print(f"❌ Challenge failed: {result['error']}")
    
    # Demo circuit gallery
    print(f"\n🖼️ Circuit Gallery Demo:")
    circuit = {
        "gates": [
            {"type": "H", "qubit": 0},
            {"type": "CNOT", "qubit": 0, "target": 1},
            {"type": "measure", "qubit": 0},
            {"type": "measure", "qubit": 1}
        ]
    }
    
    entry_id = platform.create_circuit_gallery_entry(
        alice.user_id, circuit, "My First Bell State", "A simple Bell state circuit"
    )
    print(f"✅ Circuit added to gallery: {entry_id}")
    
    # Demo leaderboard
    print(f"\n🏆 Leaderboard Demo:")
    leaderboard = platform.get_leaderboard("xp", 5)
    for entry in leaderboard:
        print(f"   {entry.rank}. {entry.user.username} - {entry.xp} XP")
    
    # Demo user profiles
    print(f"\n👤 User Profile Demo:")
    alice_profile = platform.get_user_profile(alice.user_id)
    if alice_profile:
        print(f"   User: {alice_profile['user']['username']}")
        print(f"   Level: {alice_profile['level_progress']['current_level']}")
        print(f"   XP: {alice_profile['user']['xp']}")
        print(f"   Badges: {len(alice_profile['user']['badges'])}")
    
    print(f"\n🏆 Gamified Learning Platform Demo Complete!")
    print(f"   - User Registration: ✅")
    print(f"   - Challenge System: ✅")
    print(f"   - Circuit Gallery: ✅")
    print(f"   - Leaderboards: ✅")
    print(f"   - Achievement System: ✅")

if __name__ == "__main__":
    demo_gamified_learning()
