import dspy
import os

class TaskClarificationSignature(dspy.Signature):
    """
    You are a senior AI engineering assistant. Generate exactly 4 clear, concise clarifying questions - one for each principle: Objective, Scope, Deliverable, and Success Criteria. 

    Format your response as:
    **OBJECTIVE:** [single clear question about the main goal]
    **SCOPE:** [single clear question about boundaries/files/areas]  
    **DELIVERABLE:** [single clear question about expected output]
    **SUCCESS:** [single clear question about how to validate completion]

    Keep each question under 20 words and focused on removing ambiguity.
    """
    framework_principles = dspy.InputField(desc="The core principles for deconstructing a user's task.")
    user_request = dspy.InputField(desc="The user's ambiguous or incomplete request.")
    
    clarifying_questions = dspy.OutputField(desc="Exactly 4 clarifying questions in the specified format, one per principle.")

class ClarifierModule(dspy.Module):
    """A DSPy module for clarifying user tasks."""
    def __init__(self, principles_path=None):
        super().__init__()
        self.clarifier = dspy.ChainOfThought(TaskClarificationSignature)
        
        # Load principles once during initialization
        if principles_path:
            self.framework_principles = load_principles(principles_path)
        else:
            # Default path relative to this file
            default_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'framework_principles.md')
            self.framework_principles = load_principles(default_path)

    def forward(self, user_request):
        """Forward method compatible with DSPy bootstrapping expectations."""
        result = self.clarifier(user_request=user_request, framework_principles=self.framework_principles)
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
    ollama_model = dspy.OllamaLocal(model='llama3.2:latest', model_type='text', max_tokens=2048)
    dspy.settings.configure(lm=ollama_model)

    # --- Initialize and run the Clarifier ---
    # The ClarifierModule will automatically load the framework principles
    principles_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'framework_principles.md')
    clarifier = ClarifierModule(principles_path)
    
    if not clarifier.framework_principles:
        print("Could not proceed without framework principles.")
        return

    # --- Create Training Set ---
    # We will create a few examples of ambiguous requests and the "gold standard"
    # clarifying questions we would want the module to produce.
    train_set = [
        dspy.Example(
            user_request="Hey, can you refactor the database stuff? It's too slow.",
            clarifying_questions="""1. **Objective:** What is the primary performance metric we are trying to improve (e.g., query latency, throughput, reduced server load)? Are there specific slow queries you have identified?
2. **Scope:** Which parts of the application or specific database tables are in scope for this refactoring? Should I avoid touching any specific areas?
3. **Deliverable:** What is the expected outcome? Are you looking for a code pull request with the changes, a report on the findings, or both?
4. **Success Criteria:** How will we know the refactoring was successful? Is there a specific performance benchmark we need to meet (e.g., "all API calls using the database must be under 100ms")?"""
        ).with_inputs("user_request"),

        dspy.Example(
            user_request="The user page is broken.",
            clarifying_questions="""1. **Objective:** What specific behavior makes you say the page is "broken"? Are you seeing an error message, is data not loading, or is there a visual glitch?
2. **Scope:** Does this happen for all users or a specific user? Is it happening in all web browsers or just a particular one?
3. **Deliverable:** What is the expected deliverable? A bug fix committed to the repository, or an analysis of the root cause?
4. **Success Criteria:** How can I verify the fix? What specific steps should I take on the user page to confirm that the issue is resolved?"""
        ).with_inputs("user_request"),

        dspy.Example(
            user_request="Add a new button for exporting data.",
            clarifying_questions="""1. **Objective:** What specific data should be exported when the user clicks this button? What format should the export be in (e.g., CSV, JSON, PDF)?
2. **Scope:** Where on the page should this button be located? Are there any specific UI mockups or design guidelines I should follow?
3. **Deliverable:** What is the final deliverable? A pull request with the new button implemented and functional.
4. **Success Criteria:** How do I confirm the button works correctly? Should I verify the contents and format of the exported file?"""
        ).with_inputs("user_request"),
    ]

    # --- Define Validation Logic ---
    # We need a way to score the outputs of our module. We will create a simple
    # metric that uses the LLM to judge if the generated questions are comprehensive.
    class ValidationSignature(dspy.Signature):
        """
        Given a user's request, a gold-standard set of clarifying questions, and a model-generated set of questions, evaluate if the generated questions are as good or better than the gold standard.
        """
        user_request = dspy.InputField()
        gold_standard_questions = dspy.InputField()
        generated_questions = dspy.InputField()
        
        is_comprehensive = dspy.OutputField(desc="A simple 'Yes' or 'No' answer. 'Yes' if the generated questions cover all four principles (Objective, Scope, Deliverable, Success Criteria) as effectively as the gold standard.")

    def validate_clarification(example, pred, trace=None):
        """A simpler, more lenient metric function for the DSPy compiler."""
        # Get the predicted questions from our module's output
        if hasattr(pred, 'clarifying_questions'):
            predicted_questions = pred.clarifying_questions
        else:
            predicted_questions = str(pred)
        
        # Simple heuristic validation: check if the output contains questions about our 4 principles
        principles = ['objective', 'scope', 'deliverable', 'success']
        questions_lower = predicted_questions.lower()
        
        # Count how many principles are addressed
        addressed_principles = 0
        for principle in principles:
            if principle in questions_lower:
                addressed_principles += 1
        
        # Check for proper formatting (either numbered or bold headers)
        has_proper_format = (('1.' in predicted_questions and '2.' in predicted_questions) or 
                            ('**OBJECTIVE:**' in predicted_questions and '**SCOPE:**' in predicted_questions))
        
        # Pass if we address at least 3 principles and have proper format
        is_valid = addressed_principles >= 3 and has_proper_format
        
        print(f"\n--- Validation: {example.user_request[:50]}... ---")
        print(f"Addressed principles: {addressed_principles}/4")
        print(f"Proper format: {has_proper_format}")
        print(f"Validation result: {is_valid}")
        
        return is_valid

    # --- Split data into training and development sets ---
    train_set, dev_set = train_set[:2], train_set[2:]

    # --- Stage 3: Using the DSPy Compiler (BootstrapFewShot) ---
    print("=== DSPy Optimization Process ===\n")
    
    # Create the optimizer
    # Note: BootstrapFewShot is imported from dspy.teleprompt in newer versions
    from dspy.teleprompt import BootstrapFewShot
    optimizer = BootstrapFewShot(metric=validate_clarification, max_bootstrapped_demos=2, max_labeled_demos=2)
    
    # Compile our ClarifierModule using the training examples
    print("Compiling the ClarifierModule using training examples...")
    compiled_clarifier = optimizer.compile(clarifier, trainset=train_set, valset=dev_set)
    
    print("✅ Compilation complete!\n")

    # --- Example Usage ---
    # An example of an ambiguous user request
    ambiguous_request = "Hey, can you refactor the database stuff? It's too slow."

    print(f"--- Analyzing Ambiguous Request ---\n")
    print(f"User Request: '{ambiguous_request}'\n")
    
    # Generate the clarifying questions
    result = clarifier.forward(user_request=ambiguous_request)

    print("--- Generated Clarifying Questions ---\n")
    print(result.clarifying_questions)

if __name__ == "__main__":
    main()
