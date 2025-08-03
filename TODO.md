# Agent Task Framework - TODO List

## Phase 1: Scaffolding & Initial Implementation

- [x] Set up project structure and Git repository.
- [x] Create project documentation (PRD, Technical Design, Framework Principles).
- [x] Implement the initial version of the DSPy clarifier module in `atf/main.py`.

## Phase 2: Validation & Refinement

- [ ] **In Progress:** Set up the Python virtual environment and install dependencies from `requirements.txt`.
- [ ] Run the `atf/main.py` script and validate that it connects to the Ollama model and generates clarifying questions.
- [ ] Refine the DSPy prompt and signature in `TaskClarificationSignature` to improve the quality of the generated questions.

## Phase 3: Testing & Hardening

- [ ] Build a formal test suite in the `tests/` directory to run automated checks on the clarifier's output.
- [ ] Add error handling for common failure modes (e.g., model connection issues, missing principle file).
- [ ] Implement the DSPy compiler (`BootstrapFewShot`) with examples to optimize the prompt.

## Future Work

- [ ] Explore creating a simple CLI or Web UI for easier interaction.
- [ ] Investigate packaging the tool for distribution via PyPI.
