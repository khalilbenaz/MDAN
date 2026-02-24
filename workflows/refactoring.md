# MDAN Workflow — Refactoring

> **Trigger:** When technical debt needs to be addressed without changing behavior.
> **Key Agents:** Architect Agent, Dev Agent, Test Agent

## Step 1: Pre-flight Check (Test Agent)
1. Verify existing test coverage for the target module.
2. **STOP** if coverage is inadequate. A refactor without tests is a rewrite with risks.
3. Ask the user/Dev Agent to write characterization tests if needed.

## Step 2: Design the Refactor (Architect Agent)
1. Analyze current structure and identify the code smell.
2. Propose a new, cleaner pattern (e.g., Extract Method, Replace Conditional with Polymorphism).
3. Wait for user validation.

## Step 3: Execution (Dev Agent)
1. Perform the refactoring in small, atomic steps.
2. Run the test suite after every step to ensure behavior hasn't changed.

## Step 4: Verification (Test Agent)
1. Confirm tests are passing and no new warnings have appeared.
2. Review the new code for readability.
