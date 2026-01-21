"""
User profile management
Handles loading, saving, and updating user profiles
"""
import json
from pathlib import Path
from typing import Optional
from datetime import datetime

from .schemas import UserProfile
from config import settings


class UserProfileManager:
    """Manages user profiles stored as JSON files"""

    def __init__(self, profiles_dir: Optional[Path] = None):
        self.profiles_dir = profiles_dir or settings.user_profiles_dir
        self.profiles_dir.mkdir(parents=True, exist_ok=True)

    def get_profile_path(self, user_id: str) -> Path:
        """Get the file path for a user profile"""
        return self.profiles_dir / f"{user_id}.json"

    def load_profile(self, user_id: str) -> Optional[UserProfile]:
        """Load a user profile from disk"""
        profile_path = self.get_profile_path(user_id)

        if not profile_path.exists():
            return None

        with open(profile_path, "r") as f:
            data = json.load(f)

        return UserProfile(**data)

    def save_profile(self, profile: UserProfile):
        """Save a user profile to disk"""
        profile_path = self.get_profile_path(profile.user_id)
        profile.updated_at = datetime.utcnow()

        with open(profile_path, "w") as f:
            json.dump(profile.model_dump(), f, indent=2, default=str)

    def update_constraints(
        self, user_id: str, new_constraints: dict
    ) -> UserProfile:
        """Update user constraints based on feedback"""
        profile = self.load_profile(user_id)

        if profile is None:
            raise ValueError(f"Profile not found for user_id: {user_id}")

        # Merge new constraints
        profile.constraints.update(new_constraints)
        self.save_profile(profile)

        return profile

    def create_profile(
        self,
        user_id: str,
        name: str,
        role: str,
        company: str,
        industry: str,
        topics_of_interest: list,
        delivery_email: str,
        **kwargs,
    ) -> UserProfile:
        """Create a new user profile"""
        profile = UserProfile(
            user_id=user_id,
            name=name,
            role=role,
            company=company,
            industry=industry,
            topics_of_interest=topics_of_interest,
            delivery_email=delivery_email,
            **kwargs,
        )

        self.save_profile(profile)
        return profile

    def list_profiles(self) -> list[str]:
        """List all user IDs with profiles"""
        return [
            p.stem for p in self.profiles_dir.glob("*.json")
        ]
