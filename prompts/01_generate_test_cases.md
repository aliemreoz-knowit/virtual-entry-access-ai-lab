# Prompt: Generate Integration Test Cases

> Copy this prompt into Cursor chat or Composer.

---

Act as a senior test automation engineer.

Use the following project files as context:
- `system_context.md` — system description
- `requirements.md` — unlock flow requirements
- `tests/test_unlock_flow_existing.py` — existing incomplete smoke tests

**Task:**
Create integration test cases for the unlock flow in the virtualized entry/access-control system.

**Cover the following scenarios:**
- Valid credential unlock (nominal flow)
- Invalid credential rejection
- Delayed door sensor response
- Lock unit timeout
- Gateway unavailable
- Diagnostic response delay
- Repeated unlock request during active sequence
- Communication message received out of order
- Mocked node restart during unlock sequence

**Return the result as a table with these columns:**

| Column | Description |
|--------|-------------|
| Test Case ID | Unique identifier (e.g., TC-INT-001) |
| Scenario | Short description of the test scenario |
| Category | functional / timing / diagnostic / communication / recovery |
| Preconditions | System state before the test |
| Stimulus | Action that triggers the test |
| Mocked Node Behavior | How mocked nodes behave during the test |
| Expected Result | What should happen |
| Key Assertions | Specific assertions to verify |
| Timing / Communication Assumptions | Any timing or message order assumptions |
| Automation Notes | Implementation hints or considerations |
| Local or CI | Recommended execution environment |
| Risk / Priority | High / Medium / Low |

**Constraints:**
- Do not invent real signal names, DBC names, APIs or fixture implementations.
- Use placeholders where project-specific details are missing.
- Mark assumptions clearly with `[ASSUMPTION]`.
- Keep the output reviewable by a test engineer.
- Identify which tests are suitable for local execution and which should run in CI.
- Aim for 6–8 test cases.
