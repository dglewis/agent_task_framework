#!/usr/bin/env python3
"""
Example scenarios using the Agent Task Framework.

This file demonstrates how to use the Agent Task Framework with various
real-world scenarios that could apply to any software project.
"""

import sys
import os
sys.path.append('..')

from final_instructor import FinalInstructor

def setup_dspy():
    """Configure DSPy for the examples."""
    try:
        import dspy
        ollama_model = dspy.OllamaLocal(model='llama3.2:latest', model_type='text', max_tokens=2048)
        dspy.settings.configure(lm=ollama_model)
        return True
    except Exception as e:
        print(f"❌ Error setting up DSPy: {e}")
        return False

def scenario_1_vague_request():
    """
    Scenario: User wants to improve a data processing pipeline but doesn't specify details.
    """
    print("📊 Scenario 1: Vague Data Processing Request")
    print("=" * 50)
    
    original_request = "Improve the data processing pipeline"
    
    print(f"Original Request: {original_request}")
    print("\nThis request is too vague. Let's see how the framework handles it...")
    
    instructor = FinalInstructor()
    if not instructor.initialize():
        print("❌ Failed to initialize instructor")
        return
    
    result = instructor.process_request(original_request)
    
    if result:
        print("\n✅ Framework Response:")
        print("=" * 30)
        print("Clarifying Questions Generated:")
        print(result['clarifying_questions'])
        
        if result['final_instruction']:
            print("\nDirect Instruction Available:")
            print(result['final_instruction'])
        else:
            print("\nNo direct instruction available - request too vague")
    
    print("\n" + "=" * 50 + "\n")

def scenario_2_specific_request():
    """
    Scenario: User provides a more specific request about optimizing a database.
    """
    print("🗄️  Scenario 2: Specific Database Optimization Request")
    print("=" * 50)
    
    specific_request = """Optimize the database queries in src/database/connection.py:
1. Add connection pooling
2. Implement query caching
3. Add performance monitoring
4. Output: Modified connection.py with optimizations
5. Success: 30% faster query execution time"""
    
    print(f"Specific Request: {specific_request}")
    print("\nThis request has enough details. Let's see the framework's response...")
    
    instructor = FinalInstructor()
    if not instructor.initialize():
        print("❌ Failed to initialize instructor")
        return
    
    result = instructor.process_request(specific_request)
    
    if result:
        print("\n✅ Framework Response:")
        print("=" * 30)
        print("Clarifying Questions Generated:")
        print(result['clarifying_questions'])
        
        if result['final_instruction']:
            print("\nDirect Instruction Available:")
            print(result['final_instruction'])
        else:
            print("\nNo direct instruction available")
    
    print("\n" + "=" * 50 + "\n")

def scenario_3_api_development():
    """
    Scenario: User wants to create API documentation.
    """
    print("📚 Scenario 3: API Documentation Request")
    print("=" * 50)
    
    api_request = """Create comprehensive API documentation for the user management endpoints:
- Focus on /api/users/* endpoints
- Include authentication examples
- Add error response documentation
- Output: Markdown files in docs/api/ directory
- Success: All endpoints documented with examples"""
    
    print(f"API Request: {api_request}")
    print("\nThis request is well-defined. Let's see the framework's response...")
    
    instructor = FinalInstructor()
    if not instructor.initialize():
        print("❌ Failed to initialize instructor")
        return
    
    result = instructor.process_request(api_request)
    
    if result:
        print("\n✅ Framework Response:")
        print("=" * 30)
        print("Clarifying Questions Generated:")
        print(result['clarifying_questions'])
        
        if result['final_instruction']:
            print("\nDirect Instruction Available:")
            print(result['final_instruction'])
        else:
            print("\nNo direct instruction available")
    
    print("\n" + "=" * 50 + "\n")

def scenario_4_testing_improvement():
    """
    Scenario: User wants to improve test coverage.
    """
    print("🧪 Scenario 4: Test Coverage Improvement")
    print("=" * 50)
    
    test_request = """Improve test coverage for the authentication module:
- Focus on src/auth/ directory
- Add unit tests for edge cases
- Include integration tests
- Output: New test files in tests/auth/
- Success: 90% coverage for auth module"""
    
    print(f"Test Request: {test_request}")
    print("\nThis request is specific and actionable...")
    
    instructor = FinalInstructor()
    if not instructor.initialize():
        print("❌ Failed to initialize instructor")
        return
    
    result = instructor.process_request(test_request)
    
    if result:
        print("\n✅ Framework Response:")
        print("=" * 30)
        print("Clarifying Questions Generated:")
        print(result['clarifying_questions'])
        
        if result['final_instruction']:
            print("Direct Instruction Available:")
            print(result['final_instruction'])
        else:
            print("\nNo direct instruction available")
    
    print("\n" + "=" * 50 + "\n")

def run_all_scenarios():
    """Run all example scenarios."""
    print("🎯 Agent Task Framework - Example Scenarios")
    print("=" * 60)
    print("Demonstrating how the framework handles different types of requests.")
    print()
    
    if not setup_dspy():
        print("❌ Failed to setup DSPy. Make sure Ollama is running.")
        return
    
    scenario_1_vague_request()
    scenario_2_specific_request()
    scenario_3_api_development()
    scenario_4_testing_improvement()
    
    print("✅ All scenarios completed!")
    print("\nKey Takeaways:")
    print("- Vague requests generate clarifying questions")
    print("- Specific requests can generate direct instructions")
    print("- The framework adapts to different project types")
    print("- Progressive refinement builds context iteratively")

def interactive_mode():
    """
    Interactive mode for testing custom scenarios.
    """
    print("🎯 Interactive Example Mode")
    print("=" * 40)
    print("Enter multiline requests to test the framework.")
    print("Type '###' on a new line to submit, or 'quit' to exit.")
    print()
    
    if not setup_dspy():
        print("❌ Failed to setup DSPy. Make sure Ollama is running.")
        return
    
    instructor = FinalInstructor()
    if not instructor.initialize():
        print("❌ Failed to initialize instructor")
        return
    
    while True:
        try:
            print("Enter your request (type '###' on a new line to submit, or 'quit' to exit):")
            lines = []
            while True:
                line = input()
                if line.lower().strip() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    return
                if line.strip() == "###":
                    break
                lines.append(line)
            
            request = "\n".join(lines).strip()
            if not request:
                print("❌ No request provided.")
                continue
            
            print(f"\n🔄 Processing: {request}")
            print("-" * 40)
            
            result = instructor.process_request(request)
            
            if result:
                print("\n📋 Clarifying Questions:")
                print(result['clarifying_questions'])
                
                if result['final_instruction']:
                    print("\n🚀 Direct Instruction:")
                    print(result['final_instruction'])
                else:
                    print("\n⚠️  No direct instruction available - request too vague")
            
            print("\n" + "=" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main function."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive":
            interactive_mode()
        elif sys.argv[1] == "--help":
            print("Agent Task Framework - Example Scenarios")
            print()
            print("Usage:")
            print("  python example_scenarios.py           # Run all scenarios")
            print("  python example_scenarios.py --interactive  # Interactive mode")
            print("  python example_scenarios.py --help    # Show this help")
        else:
            print("Unknown option. Use --help for usage information.")
    else:
        run_all_scenarios()

if __name__ == "__main__":
    main()