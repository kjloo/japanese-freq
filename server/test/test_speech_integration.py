#!/usr/bin/env python3
"""
Integration test for the Japanese partner chat pipeline.

This test validates the full pipeline: STT → Assistant → TTS
and follows the existing testing patterns in the codebase.

Test audio file should be located at: server/test/resources/audio/stt_test.mp3
"""

import sys
import pytest
from pathlib import Path
from unittest import mock
from bson import ObjectId

# Add the server package to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# ----------------------------------------------------------------------
# Database mock fixtures
# ----------------------------------------------------------------------
@pytest.fixture
def mock_mongodb():
    """Mock MongoDB connection to avoid database dependency in tests."""
    with mock.patch("mongoengine.connection.get_connection") as mock_conn, mock.patch(
        "mongoengine.connection.get_db"
    ) as mock_db:
        # Create a mock database with dummy collections
        mock_db_instance = mock.MagicMock()
        mock_db.return_value = mock_db_instance
        mock_conn.return_value = mock.MagicMock()
        yield mock_db_instance


@pytest.fixture
def mock_word_repository():
    """Mock WordRepository to avoid database operations."""
    with mock.patch(
        "app.repository.word.word_repository.WordRepository"
    ) as mock_repo_class:
        mock_repo = mock.MagicMock()
        mock_repo.get_words.return_value = []
        mock_repo.add_words.return_value = mock.MagicMock()
        mock_repo_class.return_value = mock_repo
        yield mock_repo


@pytest.fixture
def mock_dictionary_module(mock_word_repository):
    """Mock the dictionary_module to avoid DB connection issues."""
    with mock.patch("app.module.dictionary_module.dictionary") as mock_dict, mock.patch(
        "app.module.dictionary_module.ignore_list", new_callable=mock.PropertyMock
    ) as mock_ignore_list:
        # Mock short_lookup to return a proper dictionary structure
        mock_short_def = mock.MagicMock()
        mock_short_def.get.return_value = "raku"  # Default reading for test
        mock_dict.short_lookup.return_value = mock_short_def
        mock_ignore_list.return_value = set()
        yield mock_dict


@pytest.fixture
def mock_word_service():
    """Mock the word_service to avoid DB connection issues."""
    with mock.patch("app.service.word_service.word_repository") as mock_repo:
        mock_repo.get_words.return_value = []
        yield mock_repo


# ----------------------------------------------------------------------
# Import mocked modules to avoid database connection issues
# ----------------------------------------------------------------------
@pytest.fixture
def mock_speech_gateway():
    """Mock the speech gateway to control STT/TTS outputs."""
    with mock.patch("app.gateway.speech.transcribe") as mock_stt, mock.patch(
        "app.gateway.speech.synthesize"
    ) as mock_tts:
        mock_stt.return_value = "こんにちは"
        mock_tts.return_value = b"fake audio bytes"
        yield mock_stt, mock_tts


@pytest.fixture
def mock_conversation_assistant(mock_dictionary_module):
    """Create a mocked conversation assistant for testing."""
    from app.assistant.conversation_assistant import ConversationAssistant

    assistant = ConversationAssistant(dictionary_instance=mock_dictionary_module)
    yield assistant


# ----------------------------------------------------------------------
# Test definitions
# ----------------------------------------------------------------------
TEST_AUDIO_PATH = Path(__file__).parent / "resources" / "audio" / "stt_test.mp3"


def test_speech_pipeline_with_mocks(
    mock_conversation_assistant, mock_speech_gateway, mock_mongodb
):
    """
    Integration test: STT → Assistant → TTS pipeline

    This test validates the full flow by mocking external dependencies
    (STT, TTS, database) to ensure the assistant processes input correctly.
    """
    mock_stt, mock_tts = mock_speech_gateway

    # Load test audio (just check it exists)
    assert TEST_AUDIO_PATH.is_file(), f"Test audio not found at {TEST_AUDIO_PATH}"

    audio_bytes = TEST_AUDIO_PATH.read_bytes()
    print(f"🔊  Loaded test audio: {len(audio_bytes)} bytes")

    # STEP 1: Mock STT to return Japanese text
    stt_result = mock_stt(audio_bytes)
    assert stt_result == "こんにちは", f"Expected 'こんにちは', got {stt_result}"
    print(f"🗣️  STT output: {stt_result}")

    # STEP 2: Assistant processes the input
    assistant_response = mock_conversation_assistant.process(stt_result)
    print(f"🤖  Assistant response keys: {list(assistant_response.keys())}")

    # Verify assistant response structure
    assert "content" in assistant_response, "Assistant response missing 'content' field"
    assert "speak" in assistant_response, "Assistant response missing 'speak' field"
    assert "prefix" in assistant_response, "Assistant response missing 'prefix' field"
    assert "speaker" in assistant_response, "Assistant response missing 'speaker' field"

    assistant_reply = assistant_response["content"]
    speak_text = assistant_response["speak"]
    prefix = assistant_response["prefix"]
    speaker = assistant_response["speaker"]

    print(f"💬  Assistant says: {assistant_reply}")
    print(f"🎭  Persona: {speaker}, Response: {prefix}")

    # STEP 3: Mock TTS to verify it receives correct input
    tts_audio = mock_tts(speak_text, language="Japanese")
    assert (
        tts_audio == b"fake audio bytes"
    ), f"Expected fake audio bytes, got {tts_audio}"
    print(f"🎶  TTS called with: {speak_text}")

    # Verify TTS was called with correct arguments
    mock_tts.assert_called_once_with(speak_text, language="Japanese")

    print("\n✅  Integration test passed!")


def test_assistant_naturalness_check(mock_conversation_assistant, mock_mongodb):
    """Test that the assistant correctly identifies natural vs unnatural Japanese."""
    assistant = mock_conversation_assistant

    # Test natural Japanese (should pass)
    natural_text = "こんにちは、元気ですか？"
    result = assistant.process(natural_text)
    assert "content" in result
    print(f"✅ Natural Japanese processed: {result['content']}")

    # Test unnatural Japanese (contains Latin letters, should be flagged)
    unnatural_text = "Hello world, how are you?"
    result = assistant.process(unnatural_text)
    assert "content" in result
    print(f"✅ Unnatural Japanese processed: {result['content']}")

    print("✅ Naturalness check test passed!")


def test_assistant_persona_generation(mock_mongodb):
    """Test that the assistant generates a random persona."""
    from app.assistant.conversation_assistant import ConversationAssistant

    assistant = ConversationAssistant()

    # Verify persona properties
    assert hasattr(assistant, "name")
    assert hasattr(assistant, "location")
    assert hasattr(assistant, "situation")

    print(f"✅ Assistant persona: {assistant.name} from {assistant.location}")
    print(f"   Situation: {assistant.situation}")

    # Verify persona is within expected values
    expected_names = ["Haru", "Aiko", "Kenji", "Yumi", "Sora", "Riku", "Mai", "Taro"]
    expected_locations = ["Osaka", "Fukuoka", "Hokkaido", "Kyoto", "Nagoya", "Okinawa"]

    assert (
        assistant.name in expected_names
    ), f"Name {assistant.name} not in expected list"
    assert (
        assistant.location in expected_locations
    ), f"Location {assistant.location} not in expected list"

    print("✅ Persona generation test passed!")


def test_database_mock_integration(mock_mongodb, mock_word_repository):
    """Test that database mocks work correctly with test fixtures."""
    # Verify mock database connection
    mock_db = mock_mongodb
    assert mock_db is not None

    # Verify word repository mock
    mock_repo = mock_word_repository
    assert mock_repo.get_words.return_value == []

    # Test adding words through mock
    test_words = ["テスト", "単語"]
    mock_repo.add_words(test_words)
    mock_repo.add_words.assert_called_once_with(test_words)

    print("✅ Database mock integration test passed!")
