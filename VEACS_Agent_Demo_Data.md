# VEACS Agent Demo Data
**Virtualized Entry Access Control System — Consolidated Test Dataset**
`Workshop Use Only · All Data Synthetic · Version 1.0 · 2026-05-08`

> **Source:** [github.com/aliemreoz-knowit/virtual-entry-access-ai-lab](https://github.com/aliemreoz-knowit/virtual-entry-access-ai-lab/blob/main/VEACS_Agent_Demo_Data.md)

---

## 1. EXECUTIVE CONTEXT

The Virtualized Entry Access Control System (VEACS) is a simulated embedded platform used to validate access-control logic before deployment on physical hardware.
This test run was triggered by Pull Request #214, which introduced a new diagnostic session refresh mechanism into the Main Control Module (MCM).
The change was flagged for risk review because it modifies the timing-sensitive credential evaluation path — a core safety function.
Of the 47 tests executed, 5 failed. Three failures are directly linked to the new session-refresh behaviour; two involve environment or diagnostic handling concerns.
The primary risk is that users may experience access delays or silent credential drops under real-world idle conditions.
No physical hardware or production systems were involved. All results are from a virtualised CI environment.

---

## 2. CI RUN HISTORY

| Run ID              | Trigger                             | Total | Passed | Failed | Skipped | Environment                        |
|---------------------|-------------------------------------|------:|-------:|-------:|--------:|------------------------------------|
| CI-2026-0508-047    | PR #214 — diag-session-refresh      |    47 |     41 |      5 |       1 | CI / Docker Compose (Virtual Topo) |
| CI-2026-XXXX-XXX    | _(future run placeholder)_          |     — |      — |      — |       — | —                                  |

> **DUT:** Main Control Module (MCM) v2.4.1-rc3 · **Run duration:** 4 min 38 sec · **Date:** 2026-05-08 09:14 UTC

---

## 3. TEST RESULT OVERVIEW

| Metric              | Value   | For Charting |
|---------------------|---------|-------------:|
| Total Tests         | 47      |           47 |
| Passed              | 41      |           41 |
| Failed              | 5       |            5 |
| Skipped             | 1       |            1 |
| Pass Rate           | 87.2 %  |         87.2 |
| Failure Rate        | 10.6 %  |         10.6 |
| Skip Rate           | 2.1 %   |          2.1 |

---

## 4. FAILURE DETAILS (NORMALIZED)

| TC ID       | Category       | Scenario Summary                                           | Expected                          | Observed                                    | Suspected Area              | Blocking |
|-------------|----------------|------------------------------------------------------------|-----------------------------------|---------------------------------------------|-----------------------------|----------|
| TC-MCM-0041 | Timing         | Valid credential scanned 35 s after last transaction       | UNLOCK within 500 ms              | UNLOCK at T+812 ms (session re-init: 296 ms)| Session state machine       | Yes      |
| TC-MCM-0044 | Functional     | Two readers scan simultaneously during session refresh     | 2 access decisions returned       | CR-02 event silently dropped; 1 decision    | Credential event queue      | Yes      |
| TC-MCM-0051 | Timing         | Lock unit must ACK UNLOCK within 200 ms                    | LOCK_ACK ≤ 200 ms                 | LOCK_ACK at 204 ms; fails 6/10 runs         | Lock unit mock / host timer | No       |
| TC-MCM-0058 | Diagnostic     | Door sensor fault triggers DTC + freeze-frame capture      | DTC 0x1A4F logged with 8 B frame  | DTC logged; freeze-frame is 0 bytes         | MCM DTC handler             | No       |
| TC-MCM-0063 | Infrastructure | Gateway heartbeat stops; MCM should enter SAFE_MODE        | SAFE_MODE within 3.5 s            | MCM stays OPERATIONAL; credentials granted  | Heartbeat listener thread   | Yes      |

---

## 5. FAILURE CATEGORY BREAKDOWN

| Category       | Failures | % of Total Failures | Blocking Failures |
|----------------|:--------:|--------------------:|:-----------------:|
| Timing         |    2     |              40.0 % |         1         |
| Functional     |    1     |              20.0 % |         1         |
| Diagnostic     |    1     |              20.0 % |         0         |
| Infrastructure |    1     |              20.0 % |         1         |
| **Total**      |  **5**   |            **100 %**|       **3**       |

---

## 6. TEST ENGINEER CONFIDENCE & NOTES

### Assumptions

| # | Assumption                                                                                              |
|---|----------------------------------------------------------------------------------------------------------|
| 1 | Timing SLAs are derived from the hardware integration test plan and may not account for virtualisation overhead. |
| 2 | TC-MCM-0041 and TC-MCM-0044 exercise code paths with zero historical test coverage (new in PR #214).    |
| 3 | Freeze-frame capture (TC-MCM-0058) may be disabled by a build-time configuration flag — not yet confirmed. |
| 4 | Gateway heartbeat simulation via Docker NIC reset is a best-effort approximation of physical network loss. |
| 5 | All credential tokens are static synthetic values; real access policies are not tested.                  |

### Open Questions

| # | Question                                                                                   | Owner             | Priority |
|---|--------------------------------------------------------------------------------------------|-------------------|----------|
| 1 | Is the 500 ms SLA for TC-MCM-0041 inclusive of session refresh time, or post-session only? | System Architect  | High     |
| 2 | Should MCM emit an error frame when a credential event is dropped (TC-MCM-0044)?           | Requirements Lead | High     |
| 3 | Freeze-frame trigger point: fault detection or fault confirmation? (TC-MCM-0058)           | Diagnostic Owner  | Medium   |
| 4 | Is the heartbeat listener thread supervised by any existing task-monitor mechanism?        | MCM Dev Lead      | High     |
| 5 | Are TC-MCM-0041 and TC-MCM-0044 blocking for the current sprint release?                   | Product Owner     | High     |

### Confidence per Failure

| TC ID       | Confidence | Rationale                                                                                   |
|-------------|------------|---------------------------------------------------------------------------------------------|
| TC-MCM-0041 | High       | Fully deterministic; root cause traceable to blocking `session_refresh()` call in eval path.|
| TC-MCM-0044 | High       | Reproduces on every run; silent event drop with no error emission is a clear code defect.   |
| TC-MCM-0051 | Low        | Intermittent (6/10 runs); 4 ms overshoot is within Docker scheduler jitter; not confirmed as DUT defect. |
| TC-MCM-0058 | Medium     | DTC logging correct; freeze-frame absence may be a build config issue, not a code defect.  |
| TC-MCM-0063 | Medium     | Reproducible, but root cause involves Docker network stack interaction — not purely MCM logic. |

---

## 7. KNOWN LIMITATIONS

| # | Limitation                                                                                                     |
|---|----------------------------------------------------------------------------------------------------------------|
| 1 | **Single run only.** One CI run is available. Trends, flakiness rates, and regression history cannot be established. |
| 2 | **No hardware baseline.** All results are from a virtual environment. Timing SLA violations cannot be confirmed as real DUT defects until validated on physical hardware. |
| 3 | **TC-MCM-0051 is inconclusive.** The 4 ms overshoot falls within known mock/scheduler jitter. Filing this as a defect without hardware evidence would be premature. |
| 4 | **TC-MCM-0058 root cause is ambiguous.** The freeze-frame absence may be a build configuration omission rather than a code defect. This dataset cannot distinguish between the two. |
| 5 | **TC-MCM-0063 environment dependency.** The Docker NIC reset method is not a validated simulation of physical network loss. Results may not generalise to real deployment conditions. |
| 6 | **No coverage data.** This dataset does not include code coverage metrics. The impact of the 41 passing tests on overall coverage is unknown. |
| 7 | **No performance history.** There is no historical CI data to determine whether the 87.2 % pass rate is improving, degrading, or stable across builds. |

---

*All system names, test case IDs, DTC codes, timing values, and node identifiers are fictional.*
*This file is intended exclusively for AI workshop demonstration purposes.*
