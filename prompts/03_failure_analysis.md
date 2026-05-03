# Prompt: Failure Analysis

> Copy this prompt into Cursor chat or Composer.
> Make sure the file `logs/failed_ci_run.txt` is accessible as context.

---

Act as a senior test automation engineer and failure-analysis assistant.

Analyze the failed test results in `logs/failed_ci_run.txt`.

**Return the answer in this structure:**

1. **Executive summary** — What happened, how many tests failed, and what is the overall impact?

2. **Failure classification table** — Classify each failed test:

   | Test Case | Failure Type | Severity | Related Requirement |
   |-----------|-------------|----------|-------------------|
   | ... | functional / timing / diagnostic / infrastructure | high / medium / low | REQ-xxx |

3. **Likely root-cause hypotheses** — Provide at least 3 hypotheses for the failures. Link each to the recent code change if applicable.

4. **Evidence supporting each hypothesis** — What data in the log supports or contradicts each hypothesis?

5. **Missing information or assumptions** — What data is not available in the log? What should be collected to confirm or rule out each hypothesis?

6. **Recommended debugging steps** — Specific, actionable steps the team should take next.

7. **Suggested improvements to the tests** — How could the test suite be improved to catch or diagnose this type of issue earlier?

8. **What to report to the development team** — A concise developer-facing summary suitable for a bug report or Slack message.

**Constraints:**
- Do not claim a definitive root cause unless the evidence is sufficient.
- Mark uncertain conclusions clearly with `[UNCERTAIN]` or `[HYPOTHESIS]`.
- Separate functional failures from timing, diagnostic and infrastructure issues.
- Do not invent signal names, APIs, logs or requirements that are not in the project files.
- If more data is needed, list exactly what should be collected.
