# Resume Protocol

> MDAN-AUTO v1.0 Context Resume Procedure

## Overview

The resume protocol defines how MDAN-AUTO resumes execution from a saved context file, ensuring seamless continuation after token limits or interruptions.

## Resume Command

```bash
mdan auto resume /tmp/mdan-save-[timestamp].json
```

## Resume Process

### Step 1: Load Save File

1. Locate save file
2. Validate file exists and is readable
3. Parse JSON content
4. Validate format version

### Step 2: Validate Save State

Check:

- [ ] Version is compatible (1.0)
- [ ] All required fields present
- [ ] JSON is valid
- [ ] File is not corrupted
- [ ] Timestamp is recent (optional)

If validation fails:
- Log error
- Exit with error code
- Provide recovery instructions

### Step 3: Restore State

Restore the following:

1. **Project Information**
   - Project name
   - Description
   - Tech stack

2. **Phase State**
   - Current phase
   - Completed phases
   - Phase status

3. **Context**
   - Conversation history
   - Artifacts
   - Decisions

4. **Configuration**
   - Token limit
   - Save threshold
   - Output directory
   - Other settings

5. **Debates**
   - Debate history
   - Decisions made

6. **Quality Gates**
   - Gate status for each phase

### Step 4: Validate Environment

Check:

- [ ] Required tools installed (dotnet, docker, etc.)
- [ ] Output directory exists
- [ ] Sufficient disk space
- [ ] Network connectivity (if needed)
- [ ] API credentials valid

If environment check fails:
- Log error
- Exit with error code
- Provide setup instructions

### Step 5: Resume Execution

1. Log resume start
2. Display resume summary
3. Continue from `phases.current`
4. Increment `metadata.resume_count`
5. Execute remaining phases

## Resume Summary

Display this summary when resuming:

```
╔════════════════════════════════════════════════════════════╗
║           MDAN-AUTO v1.0 - Resume Execution               ║
╠════════════════════════════════════════════════════════════╣
║ Project: MyProject                                        ║
║ Tech Stack: C#/.NET/Blazor/SQL Server/Azure               ║
║                                                              ║
║ Current Phase: IMPLEMENT                                   ║
║ Completed: LOAD, DISCOVER, PLAN, ARCHITECT                 ║
║ Remaining: IMPLEMENT, TEST, DEPLOY, DOC                    ║
║                                                              ║
║ Save File: /tmp/mdan-save-1705310400.json                  ║
║ Save Time: 2024-01-15 10:23:45 UTC                         ║
║ Resume Count: 1                                            ║
║                                                              ║
║ Token Usage: 102,400 / 128,000 (80%)                       ║
║                                                              ║
║ Resuming execution...                                      ║
╚════════════════════════════════════════════════════════════╝
```

## Phase Resume Logic

### Resume from Pending Phase

If phase status is `pending`:
- Start phase from beginning
- Execute all phase tasks
- Mark as `in_progress`

### Resume from In-Progress Phase

If phase status is `in_progress`:
- Check for partial artifacts
- Determine last completed task
- Continue from next task
- If cannot determine, restart phase

### Resume from Failed Phase

If phase status is `failed`:
- Check error details
- Determine if recoverable
- If recoverable, retry phase
- If not recoverable, abort

### Resume from Complete Phase

If phase status is `complete`:
- Skip phase
- Move to next phase
- Verify quality gate passed

## Artifact Restoration

### File Artifacts

For each artifact in `context.artifacts`:

1. Check if file exists
2. If exists, verify content matches
3. If missing or different, recreate from saved content
4. Update file timestamps

### In-Memory Artifacts

For in-memory artifacts:
- Restore from `context.artifacts`
- Keep in memory for execution
- Save to disk when needed

## Conversation History Restoration

### History Validation

1. Validate conversation history structure
2. Check for corrupted entries
3. Remove invalid entries
4. Log any issues

### History Trimming

If conversation history is too long:
- Keep last N messages (configurable)
- Keep system messages
- Keep critical decisions
- Log trim operation

## Decision Restoration

Restore all decisions from `context.decisions`:

1. Load decision history
2. Apply decisions to current state
3. Log restored decisions
4. Use for future debates

## Quality Gate Validation

For each completed phase:

1. Check quality gate status
2. If gate failed:
   - Log warning
   - Consider re-running phase
   - Or continue with warning

## Error Handling

### Load Errors

If save file cannot be loaded:
- Log error with details
- Exit with error code 1
- Provide recovery instructions

### Validation Errors

If save state is invalid:
- Log validation errors
- Exit with error code 2
- Provide fix instructions

### Resume Errors

If resume fails:
- Log error with context
- Save current state
- Exit with error code 3
- Provide manual recovery steps

## Recovery Instructions

### Save File Not Found

```
Error: Save file not found: /tmp/mdan-save-1705310400.json

Recovery:
1. Check file path is correct
2. Look for recent saves in /tmp/
3. Use: ls -lt /tmp/mdan-save-*.json
4. If no saves found, start new execution
```

### Invalid Save Format

```
Error: Invalid save format: version mismatch

Recovery:
1. Check save file version
2. Update MDAN-AUTO to latest version
3. Or manually migrate save file
```

### Missing Artifacts

```
Error: Missing artifact: docs/discover.md

Recovery:
1. Check if artifact was saved
2. Recreate from saved content
3. Or re-run DISCOVER phase
```

### Environment Issues

```
Error: Required tool not found: dotnet

Recovery:
1. Install missing tool
2. Verify installation
3. Resume execution
```

## Resume Logging

Log all resume operations:

```
[2024-01-15 10:30:00] Starting resume from /tmp/mdan-save-1705310400.json
[2024-01-15 10:30:01] Loading save file...
[2024-01-15 10:30:02] Validating save state...
[2024-01-15 10:30:03] Restoring project state...
[2024-01-15 10:30:04] Restoring conversation history (45 messages)
[2024-01-15 10:30:05] Restoring artifacts (3 files)
[2024-01-15 10:30:06] Restoring decisions (2 decisions)
[2024-01-15 10:30:07] Validating environment...
[2024-01-15 10:30:08] Environment valid
[2024-01-15 10:30:09] Resuming from phase: IMPLEMENT
[2024-01-15 10:30:10] Resume count: 1
[2024-01-15 10:30:11] Continuing execution...
```

## Resume Count Tracking

Track resume attempts in `metadata.resume_count`:

- 0: First execution
- 1: First resume
- 2: Second resume
- etc.

If resume count > threshold (default 5):
- Log warning
- Consider aborting
- Require manual intervention

## Auto-Resume

For automatic resume after context save:

1. Detect context save
2. Wait for token limit reset
3. Automatically resume from latest save
4. Continue execution

## Manual Resume

For manual resume:

1. User provides save file path
2. Validate and load
3. Display summary
4. Ask for confirmation (optional)
5. Resume execution

## Resume Verification

After resume, verify:

- [ ] All artifacts restored
- [ ] Conversation history valid
- [ ] Decisions applied
- [ ] Environment ready
- [ ] Can continue execution

## Resume Failure Recovery

If resume fails completely:

1. Save error state
2. Provide detailed error report
3. Suggest recovery options:
   - Fix and retry resume
   - Start new execution
   - Manual intervention

## Example Resume Flow

```
1. User runs: mdan auto resume /tmp/mdan-save-1705310400.json
2. MDAN-AUTO loads save file
3. Validates save state (OK)
4. Restores project state
5. Restores conversation history
6. Restores artifacts
7. Validates environment (OK)
8. Displays resume summary
9. Resumes from IMPLEMENT phase
10. Continues execution
11. Completes remaining phases
12. MISSION COMPLETE ✅
```

## Best Practices

1. **Always validate** before resuming
2. **Log everything** for debugging
3. **Handle errors gracefully**
4. **Provide clear recovery instructions**
5. **Track resume attempts**
6. **Clean up old saves** after success
7. **Backup saves** before resume
8. **Verify environment** before resume

## Version

MDAN-AUTO Resume Protocol v1.0