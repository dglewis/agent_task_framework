# Agent Task Framework

A sophisticated tool for transforming ambiguous user requests into actionable instructions for AI agents, built with DSPy and progressive refinement.

## 🎯 Purpose

The Agent Task Framework helps you create clear, specific instructions for background agents by:
- **Analyzing request specificity** - Determines if a request has enough details
- **Generating clarifying questions** - Uses 4 core principles to identify missing information
- **Progressive refinement** - Builds context iteratively until actionable instructions emerge
- **Direct instruction generation** - Creates ready-to-use background agent instructions

## 🚀 Key Features

### ✅ **Progressive Refinement System**
- **Context Building**: Each iteration preserves and builds on previous information
- **Intelligent Threshold**: Automatically detects when enough details exist for actionable instructions
- **Iterative Intelligence**: Questions become more specific as context accumulates

### ✅ **DSPy-Powered Optimization**
- **Self-Improving Prompts**: Uses DSPy's `BootstrapFewShot` optimizer
- **Local LLM Integration**: Works with Ollama for privacy and cost control
- **Structured Output**: Generates consistent, formatted clarifying questions

### ✅ **Framework Principles**
Based on 4 core principles for task deconstruction:
1. **Objective** - What is the primary action?
2. **Scope** - What files/areas are in/out of bounds?
3. **Deliverable** - What format should the output take?
4. **Success Criteria** - How will we validate completion?

## 📦 Installation

```bash
# Clone the repository
git clone <repository-url>
cd agent_task_framework

# Install dependencies
uv sync

# Ensure Ollama is running with llama3.2:latest
ollama serve
ollama pull llama3.2:latest
```

## 🎮 Usage

### Interactive Mode
```bash
uv run python final_instructor.py
```

### Test Progressive Refinement
```bash
uv run python test_progressive.py
```

### Run Test Suite
```bash
uv run pytest
```

## 📁 Project Structure

```
agent_task_framework/
├── atf/                    # Core framework
│   ├── main.py            # DSPy clarifier module
│   └── __init__.py
├── docs/                   # Documentation
│   ├── framework_principles.md
│   ├── prd.md
│   ├── technical_design.md
│   └── tutorial_background_agents.md
├── tests/                  # Test suite
│   ├── test_clarifier.py
│   └── __init__.py
├── examples/               # Usage examples
│   └── example_scenarios.py
├── final_instructor.py     # Main application
├── test_progressive.py     # Progressive refinement tests
└── requirements.txt        # Dependencies
```

## 🔧 Core Components

### `final_instructor.py` - Main Application
- **Request Analysis**: Determines if requests are specific enough
- **Progressive Refinement**: Iterative context building
- **Instruction Generation**: Creates actionable background agent instructions

### `atf/main.py` - Core Framework
- **TaskClarificationSignature**: DSPy signature for generating questions
- **ClarifierModule**: Main DSPy module with optimization
- **Framework Principles**: Loads and applies the 4 core principles

## 📊 Current Status

- ✅ **Progressive Refinement**: Working and tested
- ✅ **DSPy Integration**: Complete with bootstrapping
- ✅ **Test Coverage**: 33% (needs improvement)
- ✅ **Documentation**: Comprehensive suite
- ✅ **Local LLM**: Ollama integration working

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=atf

# Run specific test
uv run python test_progressive.py
```

## 📈 Example Workflow

1. **Input**: `"improve the data processing pipeline"`
2. **Analysis**: Too vague, needs clarification
3. **Refinement 1**: `"Focus on data_processor.py file. Need to optimize memory usage and add error handling."`
4. **Refinement 2**: `"Output should be modified code file. Success = 50% faster processing time and no memory leaks."`
5. **Result**: `"Update the data_processor.py file to optimize memory usage, add comprehensive error handling, and ensure the pipeline processes data 50% faster without memory leaks."`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure test coverage remains high
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- **Documentation**: Check `docs/` directory
- **Examples**: See `examples/example_scenarios.py`
- **Issues**: Report bugs and feature requests via GitHub issues
