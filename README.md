# Virtual Entry / Access Control — AI Workshop Lab

A synthetic, self-contained lab repository built for workshops on AI-assisted
test engineering using **Cursor** and **Microsoft 365 Copilot**.

---

## Project Overview

This repository is a workshop-oriented training scaffold designed to give
participants a small but realistic project context to work with. It covers
practical test engineering topics such as test case generation, failure analysis,
and stakeholder communication — all within a scope that is easy to open in
Cursor and start working with immediately.

The project intentionally provides incomplete test coverage, simplified mock
classes, and a fake CI failure log so there is meaningful room for guided
AI-assisted iteration. Rather than starting from a polished test suite,
participants work through the same kinds of tasks they would face in a real
test engineering workflow: understanding the system, generating test cases,
analyzing failures, and communicating findings.

> **AI accelerates engineering work, but engineers remain responsible for
> correctness, review, safety and final decisions.**

**Note:** This repository is a training scaffold — not a production system.
All names, signals and APIs are generic placeholders. No confidential data,
real customer names, secrets, internal URLs or proprietary signal names are
included.

---

## Technical Scenario

The lab uses a **virtualized automotive entry/access-control system** based
on virtual topology testing.

| Component | Description |
|-----------|-------------|
| **DUT** | Main Control Module (MCM) / access controller |
| **Credential Reader** | Reads and sends credential events (valid or invalid) to the MCM |
| **Lock Unit** | Receives unlock commands from the MCM and sends acknowledgements |
| **Door Sensor** | Reports door state (opened / closed) to the MCM |
| **Gateway** | Routes messages between network segments (CAN ↔ Ethernet) |

**Communication:** CAN and Ethernet

**Environment:**
- Virtual topology first — all nodes run as software mocks
- No physical hardware dependency
- Tests can later move to CI and SIL/HIL environments

**Testing goal:** Validate unlock behavior, diagnostics, timing and
communication behavior before physical hardware is available.

---

## Features

- Realistic system context and requirements for a virtualized automotive ECU
- Intentionally incomplete pytest smoke tests with clear TODO markers
- Integration test skeleton with 9 empty test bodies ready for implementation
- Lightweight mock classes providing project context for Cursor
- Fake CI failure log with 18 tests (14 passed, 4 failed) for analysis
- Ready-to-use prompts for Cursor and Microsoft 365 Copilot
- Facilitator-only expected output examples
- Participant-facing lab instructions with review checklists

---

## Quick Start

### Prerequisites

- [Cursor](https://cursor.sh/) (AI-powered code editor)
- Python 3.8+ with pytest installed
- Microsoft 365 Copilot access (for Part 4)

### Opening the Lab

```bash
# Clone or download the repository
cd virtual-entry-access-ai-lab

# (Optional) Verify the smoke tests pass
pip install pytest
python -m pytest tests/ -v
```

Then open the folder in **Cursor** and follow the instructions in
`lab_instructions.md`.

---

## Project Structure

```
virtual-entry-access-ai-lab/
├── README.md                              # This file
├── system_context.md                      # System description and architecture
├── requirements.md                        # Unlock flow requirements (REQ-001 to REQ-009)
├── lab_instructions.md                    # Participant-facing step-by-step guide
├── tests/
│   ├── test_unlock_flow_existing.py       # Intentionally incomplete smoke tests
│   ├── test_unlock_flow_integration.py    # Integration test skeleton (Part 2)
│   └── conftest.py                        # Lightweight pytest fixtures
├── mocks/
│   ├── __init__.py                        # Package init
│   ├── reader.py                          # Credential Reader mock
│   ├── lock_unit.py                       # Lock Unit mock
│   ├── door_sensor.py                     # Door Sensor mock
│   └── gateway.py                         # Gateway mock
├── logs/
│   └── failed_ci_run.txt                  # Fake failed CI output for analysis
├── prompts/
│   ├── 01_generate_test_cases.md          # Cursor prompt: generate test cases
│   ├── 02_implement_test_cases.md         # Cursor prompt: implement test cases
│   ├── 03_failure_analysis.md             # Cursor prompt: analyze failures
│   └── 04_stakeholder_update.md           # M365 Copilot prompt: stakeholder update
└── expected_outputs/
    ├── example_test_case_table.md         # Facilitator reference only
    ├── example_implemented_tests.py       # Facilitator reference only
    ├── example_failure_analysis.md        # Facilitator reference only
    └── example_stakeholder_update.md      # Facilitator reference only
```

---

## Lab Workflow

The hands-on lab consists of four parts. Each part builds on the previous one.

| Part | Tool | Task | Time |
|------|------|------|------|
| **Part 1** | Cursor | Generate integration test cases from project context | ~15 min |
| **Part 2** | Cursor | Implement the generated test cases as runnable pytest code | ~15 min |
| **Part 3** | Cursor | Analyze failed CI test results | ~15 min |
| **Part 4** | Microsoft 365 Copilot | Create a stakeholder-friendly status update | ~10 min |

### Part 1 — Generate Test Cases with Cursor

**Goal:** Use Cursor to generate reviewable integration test cases.

**Input files:**
- `system_context.md` — system description
- `requirements.md` — unlock flow requirements
- `tests/test_unlock_flow_existing.py` — existing incomplete smoke tests

**Prompt:** Copy-paste from `prompts/01_generate_test_cases.md`

**Expected output:** A test case table with 6–8 test cases covering valid/invalid
credentials, timing scenarios, communication failures, and recovery scenarios.

### Part 2 — Implement Test Cases with Cursor

**Goal:** Use Cursor to implement the test case table from Part 1 as runnable
pytest code.

**Input files:**
- `tests/test_unlock_flow_integration.py` — skeleton with 9 empty test bodies
- `tests/conftest.py` — fixtures and mock wiring
- `mocks/` — mock node classes
- Your test case table from Part 1

**Prompt:** Copy-paste from `prompts/02_implement_test_cases.md`

**Expected output:** A populated test file where TC-INT-001 and TC-INT-002 pass,
and remaining tests are marked `skip` or `xfail` with clear reasons.

### Part 3 — Analyze Failed Test Results with Cursor

**Goal:** Use Cursor to analyze a fake CI test run and produce a structured
failure analysis.

**Input files:**
- `logs/failed_ci_run.txt` — fake CI output with 4 failed tests

**Prompt:** Copy-paste from `prompts/03_failure_analysis.md`

**Expected output:** Executive summary, failure classification table,
root-cause hypotheses with evidence, missing-data checklist, and debugging steps.

### Part 4 — Create Stakeholder Update with Microsoft 365 Copilot

**Goal:** Convert the technical failure analysis from Part 3 into a
stakeholder-friendly Teams/email update.

**Input:** Your output from Part 3

**Prompt:** Copy-paste from `prompts/04_stakeholder_update.md`

**Expected output:** A concise status update suitable for engineering managers,
test leads and product owners.

---

## How to Use the Prompts

All prompts are stored as markdown files in the `prompts/` directory. They are
designed to be **copied directly** into Cursor or Microsoft 365 Copilot without
modification.

### In Cursor

1. Open the repository in Cursor.
2. Open the prompt file (e.g., `prompts/01_generate_test_cases.md`).
3. Select and copy the prompt text.
4. Paste it into Cursor chat or Composer.
5. Review the generated output critically.

### In Microsoft 365 Copilot

1. Open Microsoft 365 Copilot (Teams, Word, or web).
2. Open the prompt file (e.g., `prompts/04_stakeholder_update.md`).
3. Copy the prompt text.
4. Paste your failure analysis from Part 3 into the designated area.
5. Submit and review the generated stakeholder update.

### Cursor Workflow Principle

```
Ask for a plan → Review the plan → Apply a small change → Review the diff → Iterate
```

### Safe Prompt Pattern for Larger Tasks

```
Inspect the existing tests and propose a plan first.
Do not modify files yet.
```

---

## Tool Positioning

### Cursor — Inside the Engineering Workflow

Cursor is used for tasks **inside** the engineering workflow:

- Understanding existing test code
- Generating test cases and edge cases
- Creating automation skeletons
- Refactoring test utilities
- Adding assertions and fixtures
- Analyzing failing tests and CI logs

### Microsoft 365 Copilot — Around the Engineering Workflow

Microsoft 365 Copilot is used for tasks **around** the engineering workflow:

- Documents and reports
- Meeting summaries
- Stakeholder communication
- Research and knowledge synthesis
- Follow-up actions and decision tracking

---

## Known Limitations (By Design)

These are **intentional** limitations to provide learning opportunities:

- Smoke tests are intentionally incomplete — missing timing, diagnostics and
  communication sequence assertions (`tests/test_unlock_flow_existing.py`)
- Mock classes are minimal stubs — no real simulation logic
  (`mocks/*.py`)
- The failed CI log is synthetic — designed for analysis practice, not
  a real test run (`logs/failed_ci_run.txt`)
- No real signal names, DBC definitions or project-specific APIs are used
- The VirtualTopology class uses a simple callback to wire mocks together —
  not a realistic MCM implementation (`tests/conftest.py`)
- No external dependencies beyond pytest

These are **not bugs** — they are features for workshop learning!

---

## Technology Stack

- **Language:** Python 3.8+
- **Test Framework:** pytest
- **Mocking:** Custom lightweight mock classes (no external mock library needed)
- **Environment:** Virtual topology — pure software, no hardware
- **Prompts:** Markdown files, copy-paste ready
- **Target Tools:** Cursor (AI-assisted coding), Microsoft 365 Copilot (stakeholder communication)

---

## Requirements Coverage

The repository includes 9 requirements covering the unlock flow:

| Requirement | Description | Test Coverage |
|-------------|-------------|---------------|
| REQ-001 | Valid credential unlock | Smoke test exists, incomplete |
| REQ-002 | Invalid credential rejection | Smoke test exists, incomplete |
| REQ-003 | Lock unit timeout | Not covered — generate with AI |
| REQ-004 | Delayed door sensor response | Not covered — generate with AI |
| REQ-005 | Gateway unavailable | Smoke test exists, incomplete |
| REQ-006 | Diagnostic response delay | Not covered — generate with AI |
| REQ-007 | Repeated unlock request | Not covered — generate with AI |
| REQ-008 | Message received out of order | Not covered — generate with AI |
| REQ-009 | Node restart during unlock | Not covered — generate with AI |

---

## Contributing

This is a workshop demonstration project. Feel free to:

- Fork and modify for your own workshops
- Add additional lab parts or exercises
- Improve the mock classes or test scaffolding
- Share prompts that worked well in your sessions

---

## License

This is a demo application for educational purposes. Free to use for
workshops and learning.

---

**Ready to practice AI-assisted test engineering!**

*Python + pytest | Virtual Topology | Designed for Learning | Cursor + M365 Copilot*
