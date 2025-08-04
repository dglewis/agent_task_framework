# Tutorial: Using Agent Task Framework for Background Agent Instructions

## Overview

The Agent Task Framework helps transform ambiguous user requests into clear, structured instructions that background agents can execute successfully. This tutorial shows practical examples from real project contexts.

## Why This Matters for Background Agents

Background agents work best when they have:
1. **Clear objectives** - What exactly needs to be accomplished?
2. **Defined scope** - Which files/areas to work with and which to avoid?
3. **Specific deliverables** - What output is expected?
4. **Success criteria** - How to validate the work is complete?

Without these clarifications, background agents often:
- Make incorrect assumptions
- Work on the wrong files
- Produce incomplete solutions
- Waste time and tokens on unnecessary work

## Real-World Example: Data Processing Project

### ❌ Original Ambiguous Request
```
"Improve the data processing pipeline"
```

### ✅ Framework-Generated Clarifying Questions
```
1. Deconstruct the Objective:
   - What specific improvements are needed (e.g., speed, memory usage, error handling)?
   - Should the focus be on optimization, refactoring, or adding new features?

2. Define the Operational Scope:
   - Which files in the pipeline should be modified?
   - Are there specific components to leave untouched?

3. Specify the Deliverable:
   - What format should the improvements be delivered in (modified code, new files, documentation)?
   - Should the changes be saved to specific locations?

4. Establish Success Criteria:
   - How should performance improvements be measured?
   - Are there specific benchmarks or metrics that would indicate successful improvement?
```

### 🎯 Result: Clear Background Agent Instruction
After answering the clarifying questions, you can provide a precise instruction like:

```
Optimize the data processing pipeline in `src/processing/` directory to:
1. Reduce memory usage by 30%
2. Improve processing speed by 50%
3. Add comprehensive error handling

Deliverable: Create modified files with:
- Memory optimization in data_processor.py
- Performance improvements in pipeline.py
- Error handling in error_handler.py

Success criteria: Benchmark tests show 30% memory reduction and 50% speed improvement while maintaining data accuracy.
```

## Step-by-Step Usage Guide

### 1. Installation and Setup

```bash
# Navigate to the agent_task_framework directory
cd agent_task_framework

# Install dependencies
uv install

# Ensure Ollama is running with the required model
ollama list  # Should show llama3.2:latest
```

### 2. Basic Usage

```python
from atf.main import ClarifierModule

# Initialize the framework
clarifier = ClarifierModule()

# Transform an ambiguous request
ambiguous_request = "Fix the login system"
result = clarifier.forward(user_request=ambiguous_request)

print(result.clarifying_questions)
```

### 3. Interactive Demo

```bash
# Run the demo script
python demo.py

# Or use interactive mode
python demo.py --interactive
```

## Common Background Agent Scenarios

### Scenario 1: Code Refactoring
**Original:** "Improve the scraper performance"
**Framework helps identify:**
- Which specific performance metrics to target
- Which components to refactor vs. leave untouched
- How to measure improvement
- Whether to optimize for speed, memory, or reliability

### Scenario 2: Documentation Tasks
**Original:** "Create documentation for the API"
**Framework helps identify:**
- Which API endpoints to document
- What level of detail is needed
- Target audience (developers, end-users)
- Format preferences (markdown, HTML, interactive)

### Scenario 3: Error Handling
**Original:** "Add error handling to the code"
**Framework helps identify:**
- Which modules need error handling
- Types of errors to handle
- How errors should be logged/reported
- Whether to fail gracefully or halt execution

## Integration with Cursor Background Agents

When using this framework with Cursor background agents:

1. **Start with your ambiguous request**
2. **Run it through the Agent Task Framework**
3. **Answer the generated clarifying questions**
4. **Provide the complete, structured instruction to the background agent**

### Example Workflow

```bash
# 1. Use the framework to clarify your request
python demo.py --interactive
# Input: "Optimize the database queries"

# 2. Answer the generated questions to create a complete brief

# 3. Give the background agent a detailed instruction like:
"Optimize the database queries in src/database.py focusing on the 
get_reviews() and update_sentiment() methods. Target: reduce query 
time from 2s to under 500ms. Use query profiling to identify 
bottlenecks. Deliverable: Updated code with performance benchmarks 
in comments. Success: All existing tests pass and query time 
improvement is measurable."
```

## Best Practices

### For Framework Users
1. **Be honest about ambiguity** - Don't try to over-specify initially
2. **Answer all four principle areas** - Even if some seem obvious
3. **Provide context** - Mention the project/domain when relevant
4. **Iterate if needed** - Refine based on the generated questions

### For Background Agent Instructions
1. **Include file paths** - Be specific about which files to modify
2. **Set boundaries** - Clearly state what NOT to change
3. **Provide examples** - Reference existing patterns in the codebase
4. **Define "done"** - Give measurable completion criteria

## Troubleshooting

### Framework Not Loading
- Check that Ollama is running: `ollama list`
- Ensure the model is available: `ollama pull llama3.2:latest`
- Verify you're in the correct directory with `docs/framework_principles.md`

### Poor Quality Questions
- Make sure your request has some ambiguity (the framework works best with unclear requests)
- Try rephrasing your request to be more casual/conversational
- Check that all dependencies are properly installed

### Background Agent Still Confused
- Answer ALL the generated questions before proceeding
- Be specific in your answers (avoid "whatever you think is best")
- Include concrete examples and constraints in your final instruction

## Next Steps

After mastering the basic framework:
1. Experiment with different types of requests
2. Build templates for common project patterns
3. Consider integrating the framework into your workflow automation
4. Contribute improvements and additional examples

## Support

For issues or questions:
- Check the project README and documentation
- Review the test files for additional examples
- Examine the source code in `atf/main.py` for implementation details