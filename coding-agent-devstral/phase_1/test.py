from phase_1.main import chat_stream

def test_chat_stream_returns_text():
    """Test that chat_stream returns actual LLM-generated text (not empty)."""
    response = chat_stream("What is 2+2? Respond with a number only e.g. (1,2,3,4,etc).")
    assert response is not None
    assert len(response) > 0
    # Should actually contain response, not just whitespace
    assert response.strip() == "4"
