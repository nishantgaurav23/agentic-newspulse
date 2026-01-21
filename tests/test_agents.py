"""
Tests for NewsPulse AI agents

To run tests:
    pytest tests/
"""
import pytest
from models.schemas import UserProfile, Article, Citation, Priority
from models.user_profile import UserProfileManager


class TestUserProfile:
    """Test user profile management"""

    def test_create_profile(self, tmp_path):
        """Test creating a user profile"""
        manager = UserProfileManager(profiles_dir=tmp_path)

        profile = manager.create_profile(
            user_id="test_user",
            name="Test User",
            role="CEO",
            company="Test Corp",
            industry="Technology",
            topics_of_interest=["AI", "Cloud Computing"],
            delivery_email="test@example.com",
        )

        assert profile.user_id == "test_user"
        assert profile.name == "Test User"
        assert "AI" in profile.topics_of_interest

    def test_load_profile(self, tmp_path):
        """Test loading a user profile"""
        manager = UserProfileManager(profiles_dir=tmp_path)

        # Create profile
        manager.create_profile(
            user_id="test_user",
            name="Test User",
            role="CEO",
            company="Test Corp",
            industry="Technology",
            topics_of_interest=["AI"],
            delivery_email="test@example.com",
        )

        # Load profile
        loaded = manager.load_profile("test_user")

        assert loaded is not None
        assert loaded.user_id == "test_user"

    def test_update_constraints(self, tmp_path):
        """Test updating profile constraints"""
        manager = UserProfileManager(profiles_dir=tmp_path)

        # Create profile
        manager.create_profile(
            user_id="test_user",
            name="Test User",
            role="CEO",
            company="Test Corp",
            industry="Technology",
            topics_of_interest=["AI"],
            delivery_email="test@example.com",
        )

        # Update constraints
        updated = manager.update_constraints(
            "test_user", {"length_preference": "shorter"}
        )

        assert updated.constraints["length_preference"] == "shorter"


class TestSchemas:
    """Test Pydantic schemas"""

    def test_article_requires_citations(self):
        """Test that articles must have citations"""
        with pytest.raises(ValueError):
            Article(
                title="Test Article",
                summary="Test summary",
                key_insights=["Insight 1"],
                citations=[],  # Empty citations should fail
                priority=Priority.HIGH,
                relevance_reason="Test relevance",
                url="https://example.com",
                source="example.com",
            )

    def test_citation_creation(self):
        """Test creating a citation"""
        citation = Citation(
            claim="Test claim",
            source_url="https://example.com",
            source_title="Test Article",
            quote="This is a test quote",
        )

        assert citation.claim == "Test claim"
        assert citation.source_url == "https://example.com"

    def test_article_with_valid_citations(self):
        """Test creating article with valid citations"""
        citation = Citation(
            claim="Test claim",
            source_url="https://example.com",
            source_title="Test Article",
            quote="This is a test quote",
        )

        article = Article(
            title="Test Article",
            summary="Test summary",
            key_insights=["Insight 1"],
            citations=[citation],
            priority=Priority.HIGH,
            relevance_reason="Test relevance",
            url="https://example.com",
            source="example.com",
        )

        assert len(article.citations) == 1
        assert article.priority == Priority.HIGH


# Async tests for agents
@pytest.mark.asyncio
class TestAgents:
    """Test agent functionality"""

    # Note: These tests require API keys and are integration tests
    # They are skipped by default

    @pytest.mark.skip(reason="Requires API keys")
    async def test_profile_agent(self):
        """Test profile agent"""
        from agents.profile_agent import run_profile_agent

        # This would require a real user profile
        # result = await run_profile_agent("test_user")
        # assert "user_profile" in result
        pass

    @pytest.mark.skip(reason="Requires API keys")
    async def test_search_agent(self):
        """Test search agent"""
        from agents.search_agent import run_search_agent

        # This would require API keys
        # results = await run_search_agent(["AI", "Technology"], {})
        # assert len(results) > 0
        pass


if __name__ == "__main__":
    pytest.main([__file__])
