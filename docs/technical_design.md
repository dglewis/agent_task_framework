# Technical Design Document: Agent Task Framework

## 1. Introduction

This document outlines the technical design and implementation plan for the Agent Task Framework (ATF), as defined by the requirements in `prd.md`. The primary technical challenge is to reliably and programmatically translate an ambiguous user request into a set of precise clarifying questions based on a defined framework.

## 2. Core Technology Choices

### 2.1. Language & Runtime

*   **Language:** Python 3.12+
*   **Rationale:** The modern AI/ML ecosystem, including the chosen core library, is predominantly Python-based, offering the best support and community resources.

### 2.2. Core Logic Engine: DSPy

*   **Library:** `dspy-ai`
*   **Rationale:** DSPy is chosen over simple prompt engineering for several key reasons:
    *   **Programmatic Abstraction:** It allows us to codify our `framework_principles.md` into a formal `Signature` and build a reasoning program, rather than relying on a single, complex, and brittle prompt.
    *   **Optimization & Compilation:** DSPy's `BootstrapFewShot` compiler will allow us to optimize our clarification module using a few examples. This will produce a more reliable and effective prompt than can be easily engineered by hand, leading to higher-quality question generation.
    *   **Modularity:** It encourages breaking down the reasoning process into smaller, testable components.

### 2.3. LLM Service

*   **Initial Service:** Ollama
*   **Rationale:** Ollama provides a straightforward way to serve local language models (e.g., Llama 3, Mistral). This allows for rapid, cost-effective local development and testing without reliance on external APIs. The architecture will be designed to easily swap in other model providers (e.g., OpenAI, Anthropic) in the future.

## 3. High-Level Architecture

The system will be designed as a simple Python library with a core module, `atf.clarifier`.

### 3.1. Key Components

1.  **`TaskClarificationSignature(dspy.Signature)`**:
    *   **Input:** `framework_principles: str`, `user_request: str`
    *   **Output:** `clarifying_questions: str` (A formatted string, potentially YAML or JSON, listing questions for each principle).
    *   This class formally defines the input/output contract for the LLM.

2.  **`ClarifierModule(dspy.Module)`**:
    *   This module will contain the core reasoning logic.
    *   It will initialize a `dspy.Predict` or `dspy.ChainOfThought` module using the `TaskClarificationSignature`.
    *   The `forward()` method will take a user request, load the principles from `framework_principles.md`, and execute the prediction to generate the questions.

3.  **`main.py`**:
    *   This will serve as the entry point for testing the module.
    *   It will handle setting up the DSPy environment (configuring the LLM), loading example user requests, and printing the generated clarifying questions to the console.

## 4. Development Environment

*   **Editor / IDE:** The project is being developed within a Cursor multi-root workspace, alongside the `trust-pilot-parser` project, which serves as an initial source of inspiration and use cases.
*   **Version Control:** The project resides in its own independent Git repository.
*   **Dependencies:** Managed via `requirements.txt` and installed into a virtual environment.
