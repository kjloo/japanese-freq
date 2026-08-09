#!/usr/bin/env python3
"""
Quick script to test the Japanese partner chat server setup.
This script initializes the Flask app and registers all routes.
"""

from app.module.app_module import app, register_all_blueprints


def main():
    print("🚀 Starting Japanese Partner Chat Server...")
    print("=" * 50)

    # Register all blueprints
    register_all_blueprints(app)

    print("✅ All routes registered successfully!")
    print("📝 Available endpoints:")

    # List available endpoints
    for rule in app.url_map.iter_rules():
        if rule.endpoint != "static":
            print(f"   {rule.methods} {rule.rule} -> {rule.endpoint}")

    print("=" * 50)
    print("✅ Server setup complete!")
    print("🚀 Server is ready to handle requests")
    print("   - Speech recognition: /api/speech/stt")
    print("   - Text-to-speech: /api/speech/tts")
    print("   - LLM generation: /api/llm/generate")
    print("   - Chat conversation: /api/chat/message")
    print("   - Status checks: /api/speech/status, /api/llm/status, /api/chat/status")

    # Test basic endpoint
    with app.test_client() as client:
        try:
            response = client.get("/api/chat/status")
            print("\n🔍 Quick test of /api/chat/status:")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.get_json()}")
        except Exception as e:
            print(f"\n❌ Test failed: {e}")


if __name__ == "__main__":
    main()
