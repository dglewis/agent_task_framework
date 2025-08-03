import dspy
import os

class TaskClarificationSignature(dspy.Signature):
    """
    Analyzes a user's request based on a set of framework principles and generates clarifying questions to resolve ambiguities.
    """
    framework_principles = dspy.InputField(desc="The core principles for deconstructing a user's task.")
    user_request = dspy.InputField(desc="The user's ambiguous or incomplete request.")
    
    clarifying_questions = dspy.OutputField(desc="A list of questions to clarify the user's intent, formatted as a numbered list. If no questions are needed, this should state that the request is clear.")

class ClarifierModule(dspy.Module):
    """A DSPy module for clarifying user tasks."""
    def __init__(self):
        super().__init__()
        self.clarifier = dspy.ChainOfThought(TaskClarificationSignature)

    def forward(self, user_request, principles):
        result = self.clarifier(user_request=user_request, framework_principles=principles)
        return result

def load_principles(file_path: str) -> str:
    """Loads the framework principles from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return ""

def main():
    """Main function to run the Agent Task Framework clarifier."""
    # --- Configuration ---
    # Using a local model via Ollama
    # Make sure your Ollama server is running.
    # To use a different model, change 'llama3' to the model name you have installed.
    # To use a different provider (e.g., OpenAI), change the dspy.OllamaLocal line.
    ollama_model = dspy.OllamaLocal(model='llama3.2:latest', model_type='text')
    dspy.settings.configure(lm=ollama_model)

    # --- Load Framework Principles ---
    # Assuming the script is run from the root of the 'agent_task_framework' project.
    principles_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'framework_principles.md')
    framework_principles = load_principles(principles_path)

    if not framework_principles:
        print("Could not proceed without framework principles.")
        return

    # --- Initialize and run the Clarifier ---
    clarifier = ClarifierModule()

    # --- Example Usage ---
    # An example of an ambiguous user request
    ambiguous_request = "Hey, can you refactor the database stuff? It's too slow."

    print(f"--- Analyzing Ambiguous Request ---\n")
    print(f"User Request: '{ambiguous_request}'\n")
    
    # Generate the clarifying questions
    result = clarifier.forward(user_request=ambiguous_request, principles=framework_principles)

    print("--- Generated Clarifying Questions ---\n")
    print(result.clarifying_questions)

if __name__ == "__main__":
    main()
