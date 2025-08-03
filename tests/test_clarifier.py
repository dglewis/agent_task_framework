import pytest
import dspy
import os
from atf.main import ClarifierModule, load_principles

# --- Test Configuration ---
# This is an integration test and requires a running Ollama server.
# It will use the same model as the main script.
MODEL_NAME = 'llama3.2:latest'
PRINCIPLES_PATH = os.path.join(os.path.dirname(__file__), '..', 'docs', 'framework_principles.md')

# Check if the Ollama server is accessible before running tests
try:
    ollama_model = dspy.OllamaLocal(model=MODEL_NAME, max_tokens=2048)
    dspy.settings.configure(lm=ollama_model)
    ollama_model("test connection")
    ollama_is_running = True
except Exception:
    ollama_is_running = False

@pytest.mark.skipif(not ollama_is_running, reason="Ollama server is not running or the model is not available.")
def test_clarifier_module_integration():
    """
    Tests that the ClarifierModule returns a valid, non-empty response.
    """
    # 1. Arrange
    clarifier = ClarifierModule(PRINCIPLES_PATH)
    assert clarifier.framework_principles, "Framework principles file could not be loaded."
    
    ambiguous_request = "Can you update the UI?"

    # 2. Act
    result = clarifier.forward(user_request=ambiguous_request)

    # 3. Assert
    assert result is not None, "The clarifier returned a None object."
    assert hasattr(result, 'clarifying_questions'), "The result object does not have the 'clarifying_questions' attribute."
    
    questions = result.clarifying_questions
    assert isinstance(questions, str), "The clarifying_questions attribute is not a string."
    assert len(questions.strip()) > 0, "The clarifier returned an empty string."
    
    print(f"\n--- Test Passed: Generated Questions ---\n{questions}")
