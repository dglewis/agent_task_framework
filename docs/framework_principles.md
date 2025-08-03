# Framework for Agent Task Clarification

When a user assigns a task, the agent must first deconstruct the request to ensure full comprehension before execution. If any ambiguity exists, the agent should ask clarifying questions based on the principles below. The goal is to collaboratively define a concrete, actionable plan with a predictable outcome.

## 1. Deconstruct the Objective

-   **Principle:** Clearly identify the core purpose of the task.
-   **Agent's Internal Monologue:** What is the primary action (e.g., "Refactor," "Create," "Investigate")? What is the subject of that action (e.g., "the database connection," "a new component")?
-   **Clarifying Question to User (if needed):** "To ensure I understand the main goal, you're asking me to [restate the objective in my own words]. Is that a correct summary of the intent?"

## 2. Define the Operational Scope

-   **Principle:** Establish precise boundaries for where work should be done.
-   **Agent's Internal Monologue:** Which parts of the codebase should I read from? Which am I allowed to modify? Which must I not touch?
-   **Clarifying Question to User (if needed):** "To make sure I work in the correct area, could you specify the files or directories that are in-scope for this task? Are there any I should explicitly avoid changing?"

## 3. Specify the Deliverable

-   **Principle:** The final artifact of the task must be clearly defined.
-   **Agent's Internal Monologue:** What is the expected output? A modification to an existing file? A new file with a specific name and location? A report?
-   **Clarifying Question to User (if needed):** "How would you like to receive the final output? Should I modify the code in-place, create a new file at a specific path like `docs/my_report.md`, or summarize the findings in our chat?"

## 4. Establish Success Criteria

-   **Principle:** Define how the successful completion of the task will be measured.
-   **Agent's Internal Monologue:** How will we know this is done correctly? Does a test need to pass? Does the application need to build or start successfully? Is a manual review of the output sufficient?
-   **Clarifying Question to User (if needed):** "Once I believe I'm finished, how should I validate the work? For example, should I run a specific test or command to confirm everything works as expected?" 