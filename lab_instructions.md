# Lab Instructions

Welcome to the hands-on lab! Follow the steps below in order.

> You will need **Cursor** for Parts 1, 2 and 3, and **Microsoft 365 Copilot** for Part 4.

---

## Lab Part 1 — Generate Test Cases with Cursor

### Goal

Use Cursor to generate reviewable integration test cases from the project context.

### Input files

- `system_context.md` — system description
- `requirements.md` — unlock flow requirements
- `tests/test_unlock_flow_existing.py` — existing incomplete smoke tests

### Instructions

1. Open this repository in Cursor.
2. Familiarize yourself with the three input files above.
3. Open the prompt file: `prompts/01_generate_test_cases.md`
4. Copy the prompt into Cursor chat (or Composer).
5. Review the generated test case table.
6. Check:
   - Are the scenarios relevant to the requirements?
   - Are assumptions clearly marked?
   - Are negative and timing scenarios included?
   - Would a test engineer accept this as a starting point?

### Expected deliverable

A test case table with **6–8 test cases** including:

- At least 2 negative scenarios
- At least 1 timing scenario
- At least 1 diagnostic scenario
- At least 1 communication failure scenario
- Assumptions clearly marked
- Local vs CI recommendation for each test

### Review checklist

- [ ] Test cases cover the main requirements
- [ ] Negative and edge cases are included
- [ ] Assumptions are explicitly stated
- [ ] No invented real signal names or APIs
- [ ] Output is reviewable by a test engineer
- [ ] Local vs CI recommendation is present

---

## Lab Part 2 — Implement Test Cases with Cursor

### Goal

Use Cursor to implement the test cases from your Part 1 table as runnable pytest code.

### Input files

- `tests/test_unlock_flow_integration.py` — skeleton test file with empty test bodies
- `tests/conftest.py` — fixtures and mock wiring
- `mocks/` — mock node classes with available API
- Your test case table from Part 1

### Instructions

1. Open the skeleton file: `tests/test_unlock_flow_integration.py`
2. Read the mock API reference in the module docstring.
3. Open the prompt file: `prompts/02_implement_test_cases.md`
4. Copy the prompt into Cursor chat (or Composer) — include your Part 1 test case table as context.
5. Review the generated implementation.
6. Run the tests: `python -m pytest tests/test_unlock_flow_integration.py -v`
7. Check:
   - Do TC-INT-001 and TC-INT-002 pass?
   - Are the skipped/xfail tests marked with a clear reason?
   - Are assertions specific and tied to requirements?
   - Does the GIVEN / WHEN / THEN structure make the intent clear?

### Expected deliverable

A populated `tests/test_unlock_flow_integration.py` where:

- TC-INT-001, TC-INT-002, TC-INT-005 and TC-INT-007 pass
- TC-INT-009 is marked `xfail` (behavior not yet in scaffold)
- TC-INT-003, TC-INT-004, TC-INT-006, TC-INT-008 are marked `skip` (MCM infrastructure missing)
- Each test has GIVEN / WHEN / THEN comments
- Each skip/xfail has a reason string explaining what is missing

### Review checklist

- [ ] Tests are runnable (`pytest` does not crash on collection)
- [ ] TC-INT-001 and TC-INT-002 pass
- [ ] Skipped/xfail tests have clear reason strings
- [ ] No invented mock methods used
- [ ] Assertions map directly to requirements
- [ ] GIVEN / WHEN / THEN structure is present

---

## Lab Part 3 — Analyze Failed Test Results with Cursor

### Goal

Use Cursor to analyze a failed CI test run and produce a structured failure analysis.

### Input files

- `logs/failed_ci_run.txt` — fake failed CI output

### Instructions

1. Open the failed CI log: `logs/failed_ci_run.txt`
2. Read through the failures and the observed message sequence.
3. Open the prompt file: `prompts/03_failure_analysis.md`
4. Copy the prompt into Cursor chat (or Composer).
5. Review the generated failure analysis.
6. Check:
   - Is the root-cause reasoning sound?
   - Are uncertain conclusions marked clearly?
   - Are functional, timing and diagnostic issues separated?
   - Is the missing-data checklist actionable?

### Expected deliverable

A structured failure analysis including:

- Executive summary
- Failure classification table
- 3 likely root-cause hypotheses with supporting evidence
- Missing-data checklist
- Recommended debugging steps
- Developer-facing summary

### Review checklist

- [ ] Executive summary is concise and accurate
- [ ] Failures are classified (functional / timing / diagnostic / infrastructure)
- [ ] Root-cause hypotheses are supported by evidence
- [ ] Uncertainty is clearly marked
- [ ] Missing data is identified
- [ ] Debugging steps are actionable
- [ ] No invented data or signal names

---

## Lab Part 4 — Create Stakeholder Update with Microsoft 365 Copilot

### Goal

Use Microsoft 365 Copilot to convert the technical failure analysis into a stakeholder-friendly status update.

### Input

Use the **output from Lab Part 3** as input.

### Instructions

1. Open Microsoft 365 Copilot (Teams, Word, or web).
2. Open the prompt file: `prompts/04_stakeholder_update.md`
3. Copy the prompt into Microsoft 365 Copilot.
4. Paste your failure analysis from Part 2 as the input context.
5. Review the generated stakeholder update.
6. Check:
   - Is the tone appropriate for managers and product owners?
   - Are facts separated from assumptions?
   - Is the release risk assessment reasonable?
   - Are next actions clear?

### Expected deliverable

A stakeholder-friendly update suitable for a Teams message or email, including:

- Current test status
- Main failure pattern
- Release risk assessment
- What is known vs what is uncertain
- Recommended next actions
- Open questions

### Review checklist

- [ ] Tone is clear, neutral and concise
- [ ] Suitable for engineering manager, test lead and product owner
- [ ] Facts and assumptions are separated
- [ ] Root cause is not overstated
- [ ] Next actions are specific
- [ ] No invented data
- [ ] Could be sent as-is via Teams or email

---

## Tips

- You can iterate on prompts — refine and re-run if the first result is not satisfactory.
- Compare your output with the examples in `expected_outputs/` (facilitator reference).
- Remember: AI output is a **starting point**, not a final deliverable. Your review and judgment are essential.
