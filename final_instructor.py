#!/usr/bin/env python3
"""
Final Instructor - Direct path to background agent instructions.

Simpler approach: Always generate both analysis AND final instruction, 
then let the user choose which one to use.

Usage:
    python final_instructor.py
"""

import os
import sys
import dspy
from atf.main import ClarifierModule

class RequestAnalysisSignature(dspy.Signature):
    """
    Analyze if a request has enough specific details to create actionable instructions.
    Only return YES if the request mentions specific files, technologies, or concrete tasks.
    Return NO for vague requests that would require making up details.
    """
    user_request = dspy.InputField(desc="The user's request for a background agent task")
    
    has_specifics = dspy.OutputField(desc="YES if request mentions specific files, paths, technologies, or concrete tasks. NO if too vague and would require inventing details.")
    reasoning = dspy.OutputField(desc="Brief explanation of what specific details are present or missing.")

class FinalInstructionSignature(dspy.Signature):
    """
    Convert a detailed user request into a high-level, actionable instruction for a background agent.
    
    CRITICAL RULES:
    - Use ONLY facts explicitly stated in the request
    - Provide high-level steps, not specific commands
    - Do NOT assume libraries, tools, or implementation details
    - Do NOT invent file formats, data structures, or technical specifics
    - Focus on WHAT to accomplish, not HOW to implement
    """
    user_request = dspy.InputField(desc="The user's detailed request")
    
    final_instruction = dspy.OutputField(desc="A high-level, fact-based instruction that tells the agent WHAT to accomplish using only details from the request. No assumptions about tools, libraries, or implementation methods.")

class FinalInstructor:
    def __init__(self):
        self.clarifier = None
        self.instruction_generator = None
        self.analyzer = None
        
    def setup_dspy(self):
        """Configure DSPy with Ollama model."""
        try:
            ollama_model = dspy.OllamaLocal(model='llama3.2:latest', model_type='text', max_tokens=2048)
            dspy.settings.configure(lm=ollama_model)
            return True
        except Exception as e:
            print(f"❌ Error connecting to Ollama: {e}")
            print("Make sure Ollama is running with: ollama serve")
            return False
    
    def initialize(self):
        """Initialize all components."""
        if not self.setup_dspy():
            return False
            
        self.clarifier = ClarifierModule()
        if not self.clarifier.framework_principles:
            print("❌ Error: Could not load framework principles.")
            return False
            
        self.instruction_generator = dspy.ChainOfThought(FinalInstructionSignature)
        self.analyzer = dspy.ChainOfThought(RequestAnalysisSignature)
        
        return True
    
    def get_multiline_input(self, prompt):
        """Get multiline input from user using ### as end marker."""
        print(f"{prompt} (type '###' on a new line to submit):")
        lines = []
        while True:
            line = input()
            if line.strip() == "###":
                break
            lines.append(line)
        return "\n".join(lines).strip()
    
    def process_request(self, user_request):
        """Process a user request and provide both options."""
        print("🔄 Processing your request...\n")
        
        try:
            # First, analyze if request has enough specifics
            print("🔍 Analyzing request specificity...")
            analysis = self.analyzer(user_request=user_request)
            
            # Always generate clarifying questions
            print("1️⃣ Generating clarifying questions...")
            clarifying_result = self.clarifier.forward(user_request=user_request)
            
            # Only generate final instruction if request has specifics
            final_result = None
            if "YES" in analysis.has_specifics.upper():
                print("2️⃣ Generating direct instruction...")
                final_result = self.instruction_generator(user_request=user_request)
            else:
                print("2️⃣ Request too vague for direct instruction (would require inventing details)")
                print(f"   Reason: {analysis.reasoning}")
            
            print("\n" + "=" * 60)
            print("📋 OPTION 1: CLARIFYING QUESTIONS")
            print("=" * 60)
            print("Use these if you want to refine your request further:\n")
            print(clarifying_result.clarifying_questions)
            
            if final_result:
                print("\n" + "=" * 60)
                print("🚀 OPTION 2: READY-TO-USE INSTRUCTION")
                print("=" * 60)
                print("Copy this directly to your background agent:\n")
                print(final_result.final_instruction)
                print("=" * 60)
            else:
                print("\n" + "=" * 60)
                print("🚀 OPTION 2: NOT AVAILABLE")
                print("=" * 60)
                print("Request is too vague to create actionable instructions.")
                print("Please use the clarifying questions above to add more details.")
                print("=" * 60)
            
            return {
                'clarifying_questions': clarifying_result.clarifying_questions,
                'final_instruction': final_result.final_instruction if final_result else None
            }
                
        except Exception as e:
            print(f"❌ Error processing request: {e}")
            return None
    
    def interactive_mode(self):
        """Interactive mode for processing requests."""
        print("🎯 Final Instructor - Direct Background Agent Instructions")
        print("=" * 60)
        print("Get both clarifying questions AND a ready-to-use instruction.")
        print("Choose what works best for your situation.\n")
        
        while True:
            try:
                user_request = self.get_multiline_input("📝 Enter your background agent request")
                
                if not user_request:
                    print("Please enter a request.\n")
                    continue
                    
                if user_request.lower().strip() in ['quit', 'exit']:
                    print("👋 Goodbye!")
                    break
                
                print(f"\n📥 Processing request ({len(user_request)} characters)...\n")
                
                result = self.process_request(user_request)
                
                if result:
                    has_instruction = result['final_instruction'] is not None
                    
                    print("\n💡 Which option do you prefer?")
                    print("  1. Use the clarifying questions to refine your request")
                    if has_instruction:
                        print("  2. Use the ready-to-use instruction as-is")
                        print("  3. Save both to a file")
                    else:
                        print("  2. Save clarifying questions to a file")
                        print("     (No ready-to-use instruction available - request too vague)")
                    
                    choice = input("\nEnter your choice (1-3): ").strip()
                    
                    if choice == "1":
                        # Progressive refinement workflow
                        current_request = user_request
                        refinement_count = 1
                        
                        while True:
                            print(f"\n🔄 REFINEMENT MODE - Round {refinement_count}")
                            print("Answer the clarifying questions to improve your request:")
                            print("-" * 50)
                            
                            # Show the current state
                            print(f"📋 Current Request:\n{current_request}\n")
                            print("🤔 Clarifying Questions to Answer:")
                            print(result['clarifying_questions'])
                            print()
                            
                            answers = self.get_multiline_input("📝 Provide answers to any/all of the questions above")
                            
                            if answers:
                                # Progressively build the request
                                current_request = f"{current_request}\n\n[Refinement {refinement_count}]: {answers}"
                                print(f"\n🔄 Processing refined request (Round {refinement_count})...")
                                
                                # Process the enhanced request
                                refined_result = self.process_request(current_request)
                                if refined_result:
                                    if refined_result['final_instruction']:
                                        print(f"\n✅ Refinement successful after {refinement_count} round(s)!")
                                        print("You now have a ready-to-use instruction.")
                                        break
                                    else:
                                        print(f"\n⚠️  Still needs more details. Let's continue refining...")
                                        result = refined_result  # Update for next iteration
                                        refinement_count += 1
                                        
                                        if refinement_count > 3:
                                            print("\n🛑 Reached maximum refinement rounds (3).")
                                            print("The request may be too complex for this tool.")
                                            break
                                else:
                                    print("\n❌ Error processing refined request.")
                                    break
                            else:
                                print("\n❌ No answers provided. Exiting refinement mode.")
                                break
                    
                    elif choice == "2" and not has_instruction:
                        # Save just clarifying questions for vague requests
                        filename = input("Enter filename (default: clarifying_questions.txt): ").strip()
                        if not filename:
                            filename = "clarifying_questions.txt"
                        
                        try:
                            with open(filename, 'w') as f:
                                f.write("# Background Agent Task - Clarifying Questions\n\n")
                                f.write(f"## Original Request\n{user_request}\n\n")
                                f.write(f"## Clarifying Questions\n{result['clarifying_questions']}\n\n")
                                f.write("## Next Steps\nAnswer the questions above and re-run with more details.\n")
                            print(f"✅ Saved clarifying questions to {filename}")
                        except Exception as e:
                            print(f"❌ Error saving file: {e}")
                    
                    elif choice == "3" or (choice == "2" and has_instruction):
                        filename = input("Enter filename (default: agent_task.txt): ").strip()
                        if not filename:
                            filename = "agent_task.txt"
                        
                        try:
                            with open(filename, 'w') as f:
                                f.write("# Background Agent Task\n\n")
                                f.write(f"## Original Request\n{user_request}\n\n")
                                f.write(f"## Clarifying Questions\n{result['clarifying_questions']}\n\n")
                                if result['final_instruction']:
                                    f.write(f"## Ready-to-Use Instruction\n{result['final_instruction']}\n")
                                else:
                                    f.write("## Ready-to-Use Instruction\nNot available - request too vague.\n")
                            print(f"✅ Saved to {filename}")
                        except Exception as e:
                            print(f"❌ Error saving file: {e}")
                    
                    elif choice == "2":
                        if result['final_instruction']:
                            print("\n📋 Ready-to-use instruction (copy this):")
                            print("-" * 40)
                            print(result['final_instruction'])
                            print("-" * 40)
                        else:
                            print("\n❌ No ready-to-use instruction available.")
                            print("The request was too vague. Please try option 1 to refine it.")
                
                print("\n" + "=" * 60 + "\n")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}\n")

def main():
    """Main function."""
    instructor = FinalInstructor()
    
    if not instructor.initialize():
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Test with your detailed request
        detailed_request = """Analyze reviews in samples/tp_dea_reviews.json to identify:
1. Sentiment distribution across star ratings
2. Top 3 complaint categories  
3. Keywords that correlate with negative reviews

Output: Create analysis_results.json with findings and supporting statistics.
Files to modify: Only create new files in output/ directory.
Success criteria: Report includes at least 50 review samples and actionable insights."""
        
        print("🧪 Testing with detailed request...")
        instructor.process_request(detailed_request)
    else:
        instructor.interactive_mode()

if __name__ == "__main__":
    main()