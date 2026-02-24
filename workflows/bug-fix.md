# MDAN Workflow — Bug Fix

> **Trigger:** When a bug is reported in an existing feature.
> **Key Agents:** Dev Agent, Test Agent

## Step 1: Reproduction (Dev Agent)
1. Ask the user for steps to reproduce.
2. If possible, write a failing unit/integration test that captures the bug.
3. Confirm the test fails.

## Step 2: Root Cause Analysis (Dev Agent)
1. Trace the execution path.
2. Identify the exact line or logic block causing the issue.
3. Explain the "Why" to the user briefly.

## Step 3: Fix (Dev Agent)
1. Implement the fix.
2. Ensure the previously written test now passes.

## Step 4: Verification (Test Agent & Security Agent)
1. Ask the Test Agent to review the fix for edge cases or regression risks.
2. Ask the Security Agent to ensure the fix didn't introduce a vulnerability (e.g., bypass authorization).

## Step 5: Wrap up (Orchestrator)
1. Update `MDAN-STATE.json` if this bug was tracked as an issue.
2. Ask the user if they want to deploy the fix immediately or batch it.
