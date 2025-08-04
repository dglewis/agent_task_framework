#!/usr/bin/env python3
"""
Test script to validate progressive refinement functionality
"""
import sys
sys.path.append('.')

from final_instructor import FinalInstructor

def test_progressive_refinement():
    """Test the progressive refinement logic"""
    print("🧪 Testing Progressive Refinement Logic")
    print("=" * 50)
    
    # Initialize
    fi = FinalInstructor()
    if not fi.initialize():
        print("❌ Failed to initialize FinalInstructor")
        return False
    
    print("✅ DSPy setup successful")
    
    # Verify all modules are initialized
    print(f"   Clarifier: {fi.clarifier is not None}")
    print(f"   Analyzer: {fi.analyzer is not None}")
    print(f"   Instruction Generator: {fi.instruction_generator is not None}")
    
    # Test 1: Initial vague request
    initial_request = "make the parser compliant with robot.txt"
    print(f"\n📝 Initial Request: {initial_request}")
    
    result1 = fi.process_request(initial_request)
    if not result1:
        print("❌ Failed to process initial request")
        return False
    
    print(f"✅ Initial processing: Has instruction = {result1['final_instruction'] is not None}")
    
    # Test 2: Progressive refinement (simulating what happens in the loop)
    refinement_1 = "Focus on data_processor.py file. Need to optimize memory usage and add error handling."
    current_request = f"{initial_request}\n\n[Refinement 1]: {refinement_1}"
    
    print(f"\n🔄 After Refinement 1:")
    print(f"Current Request: {current_request}")
    
    result2 = fi.process_request(current_request)
    if not result2:
        print("❌ Failed to process refined request")
        return False
    
    print(f"✅ Refinement 1 processing: Has instruction = {result2['final_instruction'] is not None}")
    
    # Test 3: Further refinement
    refinement_2 = "Output should be modified data_processor.py with optimizations. Success = 50% faster processing time and no memory leaks."
    current_request = f"{current_request}\n\n[Refinement 2]: {refinement_2}"
    
    print(f"\n🔄 After Refinement 2:")
    print(f"Current Request: {current_request}")
    
    result3 = fi.process_request(current_request)
    if not result3:
        print("❌ Failed to process second refined request")
        return False
    
    print(f"✅ Refinement 2 processing: Has instruction = {result3['final_instruction'] is not None}")
    
    # Show final instruction if available
    if result3['final_instruction']:
        print(f"\n🎯 Final Instruction Generated:")
        print("-" * 40)
        print(result3['final_instruction'])
        print("-" * 40)
    
    print(f"\n📊 Test Summary:")
    print(f"   Initial request → Instruction: {result1['final_instruction'] is not None}")
    print(f"   After refinement 1 → Instruction: {result2['final_instruction'] is not None}")
    print(f"   After refinement 2 → Instruction: {result3['final_instruction'] is not None}")
    
    return True

if __name__ == "__main__":
    try:
        success = test_progressive_refinement()
        if success:
            print("\n✅ Progressive refinement test completed")
        else:
            print("\n❌ Progressive refinement test failed")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()