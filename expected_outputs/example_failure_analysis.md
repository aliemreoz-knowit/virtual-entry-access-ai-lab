# Example: Failure Analysis

> **Facilitator reference only.** Do not share with participants before the exercise.
> This is an example of what a good AI-generated failure analysis might look like.
> Participant outputs will vary.

---

## 1. Executive Summary

4 out of 18 tests failed in CI run #1247 on branch `feature/unlock-timeout-refactor`. All failures are related to timing behavior and error handling in the unlock flow. The recent commit `a3f8c21` refactored unlock-flow timeout handling, which is the most likely trigger. No infrastructure issues were observed — all failures appear to be functional or timing regressions.

---

## 2. Failure Classification

| Test Case | Failure Type | Severity | Related Requirement |
|-----------|-------------|----------|-------------------|
| TC-UNLOCK-003 | Timing | High | REQ-004 (door sensor timeout) |
| TC-UNLOCK-004 | Functional | High | REQ-003 (lock unit timeout diagnostic) |
| TC-UNLOCK-006 | Timing | Medium | REQ-006 (diagnostic response delay) |
| TC-UNLOCK-008 | Functional / Safety | High | REQ-009 (node restart handling) |

---

## 3. Likely Root-Cause Hypotheses

### Hypothesis A — Timeout thresholds were changed during the refactor [HYPOTHESIS]

The refactor may have altered timeout values or the mechanism that detects timeouts. This would explain why TC-003 and TC-006 fail with delayed responses that previously passed.

### Hypothesis B — Diagnostic event emission was broken [HYPOTHESIS]

TC-004 expects a `LOCK_UNIT_TIMEOUT` diagnostic but none was raised. The refactor may have removed or bypassed the code path that emits diagnostics on timeout.

### Hypothesis C — Stale state not cleared on node restart [HYPOTHESIS]

TC-008 shows that an unlock command was sent after the Reader reconnected, suggesting the MCM resumed a stale unlock sequence instead of aborting it. The refactor may have changed how the MCM handles reconnection during an active sequence.

---

## 4. Evidence

| Hypothesis | Supporting Evidence | Contradicting Evidence |
|-----------|-------------------|----------------------|
| A — Thresholds changed | TC-003: 820 ms vs 500 ms limit; TC-006: 1450 ms vs 1000 ms limit. Both exceed thresholds by similar margins (~60–45%). | TC-010, TC-011, TC-012 passed — nominal timing is still OK. |
| B — Diagnostic emission broken | TC-004: empty diagnostic events list. | TC-003 and TC-006 failures are timing-based, not missing diagnostics. Diagnostic system may be partially working. |
| C — Stale state on restart | TC-008 message sequence shows `unlock_command_sent_to_lock_unit` at T+410 ms, after `reader_reconnected` at T+340 ms. | Only one test covers this scenario — could be edge case. |

---

## 5. Missing Information

- [ ] Diff of commit `a3f8c21` — what exactly was changed in the timeout handling?
- [ ] MCM internal logs — are timeout events being detected but not emitted?
- [ ] Previous CI run results — did these tests pass on the commit before `a3f8c21`?
- [ ] Timeout configuration values — were threshold constants changed?
- [ ] MCM state machine — does the restart handling code reference the new timeout logic?

---

## 6. Recommended Debugging Steps

1. Review the diff of `a3f8c21` and identify changes to timeout constants, timer initialization, and diagnostic emission code.
2. Run TC-004 locally with verbose MCM logging to check whether the timeout is detected internally but not emitted.
3. Run TC-008 locally and inspect the MCM state after `reader_reconnected` — check whether the unlock sequence was properly aborted.
4. Compare timing values from a passing CI run (pre-refactor) against the current run.
5. Check whether the timeout refactor introduced a race condition between timer expiration and event processing.

---

## 7. Suggested Test Improvements

- Add MCM internal state logging to timing-related tests to distinguish "timeout not detected" from "timeout detected but diagnostic not emitted."
- Add a test that verifies the MCM state machine transitions on node disconnect/reconnect.
- Add boundary tests at exactly the timeout threshold (e.g., 499 ms and 501 ms for door sensor) to catch off-by-one errors.
- Consider adding a regression tag for tests affected by timeout logic.

---

## 8. Developer-Facing Summary

> **4 test failures in CI after unlock-timeout refactor (`a3f8c21`)**
>
> **What failed:** Door sensor timing (TC-003), lock unit timeout diagnostic missing (TC-004), diagnostic response timing (TC-006), stale unlock after node restart (TC-008).
>
> **Likely cause:** The timeout refactor appears to have changed timing thresholds and/or broken diagnostic event emission. TC-008 suggests stale state is not cleared on node restart.
>
> **Action needed:** Review the diff of `a3f8c21`, check timeout constants, and verify diagnostic emission paths. TC-008 may indicate a safety-relevant regression.
>
> **Severity:** High — recommend blocking merge until TC-004 and TC-008 are resolved.
