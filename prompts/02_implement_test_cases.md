# Prompt: Implement Integration Test Cases

> Copy this prompt into Cursor chat or Composer.
> Make sure the following files are accessible as context before running the prompt.

---

Act as a senior test automation engineer.

Use the following project files as context:
- `tests/test_unlock_flow_integration.py` — skeleton test file with empty test bodies
- `tests/conftest.py` — pytest fixtures and VirtualTopology wiring
- `mocks/reader.py`, `mocks/lock_unit.py`, `mocks/door_sensor.py`, `mocks/gateway.py` — mock node API
- The test case table you generated in Part 1 — use it as the specification for each test

**Task:**
Implement the test bodies in `tests/test_unlock_flow_integration.py`.

**For each test:**
1. Use the GIVEN / WHEN / THEN comment structure.
2. Call only methods that exist on the mock classes (see mock API in the docstring at the top of the skeleton file).
3. Write clear assertions that directly verify the expected result from the test case table.
4. For tests that require MCM behavior not yet modeled in the scaffold (timer logic, diagnostics, in-progress state), use `@pytest.mark.skip(reason="...")` or `@pytest.mark.xfail(reason="...")` with a clear explanation.

**Constraints:**
- Do not invent new mock methods that do not exist yet.
- Do not modify `conftest.py` or the mock classes.
- Use `time.monotonic()` for timing assertions where applicable.
- Keep each test focused on a single scenario.
- Mark tests that cannot be fully implemented yet — but still write the assertion that *would* be correct once the MCM is implemented.
- `@pytest.mark.skip` — use when the test cannot run at all without missing infrastructure.
- `@pytest.mark.xfail(strict=True)` — use when the test can run but is expected to fail because the behavior is not yet implemented in `VirtualTopology`.
