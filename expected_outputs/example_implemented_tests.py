"""
Integration tests for the unlock flow — expected output example.

> Facilitator reference only. Do not share with participants before the exercise.
> This is an example of what a good Cursor-assisted implementation might look like.
> Participant outputs will vary.
"""

import time
import pytest


# ---------------------------------------------------------------------------
# TC-INT-001 — Nominal unlock flow
# ---------------------------------------------------------------------------

def test_nominal_unlock_valid_credential(virtual_topology, reader, lock_unit, door_sensor, gateway):
    # GIVEN: system running, locked, gateway available
    virtual_topology.start()
    lock_unit.set_locked()
    gateway.set_available()

    # WHEN: valid credential presented and full sequence executes
    start = time.monotonic()
    reader.send_valid_credential()
    lock_unit.acknowledge_unlock()
    door_sensor.report_door_opened()
    elapsed_ms = (time.monotonic() - start) * 1000

    # THEN: all sequence steps completed; system unlocked; timing within limit
    assert lock_unit.received_unlock_command()
    assert lock_unit.has_acknowledged
    assert door_sensor.reported_door_opened()
    assert not lock_unit.is_locked
    assert elapsed_ms < 2000, f"Sequence took {elapsed_ms:.1f} ms, expected < 2000 ms (REQ-001)"


# ---------------------------------------------------------------------------
# TC-INT-002 — Invalid credential rejection
# ---------------------------------------------------------------------------

def test_invalid_credential_no_unlock(virtual_topology, reader, lock_unit):
    # GIVEN: system running, locked
    virtual_topology.start()
    lock_unit.set_locked()

    # WHEN: invalid credential presented
    reader.send_invalid_credential()

    # THEN: no unlock command sent; lock remains locked; diagnostic recorded
    assert not lock_unit.received_unlock_command()
    assert lock_unit.is_locked
    assert "INVALID_CREDENTIAL_REJECTED" in virtual_topology.diagnostics


# ---------------------------------------------------------------------------
# TC-INT-003 — Delayed door sensor timeout
# ---------------------------------------------------------------------------

@pytest.mark.skip(
    reason="TC-INT-003: Requires MCM timer logic and virtual clock — "
           "DOOR_SENSOR_TIMEOUT diagnostic is not modeled in the current VirtualTopology scaffold."
)
def test_delayed_door_sensor_timeout(virtual_topology, reader, lock_unit, door_sensor):
    # GIVEN: credential accepted and lock acknowledged; door sensor silent
    virtual_topology.start()
    lock_unit.set_locked()
    reader.send_valid_credential()
    lock_unit.acknowledge_unlock()
    # door_sensor.report_door_opened() deliberately not called within 500 ms

    # THEN: MCM should raise DOOR_SENSOR_TIMEOUT; system stays locked
    # [ASSUMPTION: VirtualTopology would need timer logic to emit this diagnostic automatically]
    assert "DOOR_SENSOR_TIMEOUT" in virtual_topology.diagnostics
    assert lock_unit.is_locked


# ---------------------------------------------------------------------------
# TC-INT-004 — Lock unit timeout (no acknowledgement)
# ---------------------------------------------------------------------------

@pytest.mark.skip(
    reason="TC-INT-004: Requires MCM timer logic — "
           "LOCK_UNIT_TIMEOUT diagnostic is not modeled in the current VirtualTopology scaffold."
)
def test_lock_unit_timeout_no_ack(virtual_topology, reader, lock_unit, door_sensor):
    # GIVEN: valid credential presented; lock unit receives command but does not acknowledge
    virtual_topology.start()
    lock_unit.set_locked()
    reader.send_valid_credential()
    # lock_unit.acknowledge_unlock() deliberately not called

    # THEN: MCM should raise LOCK_UNIT_TIMEOUT; door should not open
    # [ASSUMPTION: VirtualTopology would need timer logic to emit this diagnostic automatically]
    assert "LOCK_UNIT_TIMEOUT" in virtual_topology.diagnostics
    assert not door_sensor.reported_door_opened()
    assert lock_unit.is_locked


# ---------------------------------------------------------------------------
# TC-INT-005 — Gateway unavailable blocks unlock
# ---------------------------------------------------------------------------

def test_gateway_unavailable_blocks_unlock(virtual_topology, reader, lock_unit, gateway):
    # GIVEN: system running, gateway unavailable
    virtual_topology.start()
    lock_unit.set_locked()
    gateway.set_unavailable()

    # WHEN: valid credential presented
    reader.send_valid_credential()

    # THEN: unlock command must NOT reach lock unit; system stays locked; diagnostic raised
    assert not lock_unit.received_unlock_command(), (
        "MCM sent unlock command despite gateway being unavailable (REQ-005)"
    )
    assert lock_unit.is_locked
    assert "GATEWAY_UNAVAILABLE" in virtual_topology.diagnostics


# ---------------------------------------------------------------------------
# TC-INT-006 — Diagnostic response delay
# ---------------------------------------------------------------------------

@pytest.mark.skip(
    reason="TC-INT-006: Requires MCM diagnostic request/response API with simulated latency — "
           "not yet defined in the scaffold. "
           "Implement once VirtualTopology supports timed diagnostic request/response."
)
def test_diagnostic_response_delay_flagged(virtual_topology):
    # GIVEN: system running, idle
    virtual_topology.start()

    # WHEN: diagnostic request sent; response time measured
    # [ASSUMPTION: VirtualTopology would need a request_diagnostic() API with simulated latency]
    start = time.monotonic()
    response = virtual_topology.request_diagnostic()
    elapsed_ms = (time.monotonic() - start) * 1000

    # THEN: response received; violations over 1000 ms flagged
    assert response is not None
    if elapsed_ms > 1000:
        pytest.fail(
            f"Diagnostic response took {elapsed_ms:.1f} ms — exceeds 1000 ms threshold (REQ-006)"
        )


# ---------------------------------------------------------------------------
# TC-INT-007 — Repeated unlock request during active sequence
# ---------------------------------------------------------------------------

def test_repeated_unlock_request_rejected(virtual_topology, reader, lock_unit):
    # GIVEN: first sequence started (unlock_command sent, ack not yet received)
    virtual_topology.start()
    lock_unit.set_locked()
    reader.send_valid_credential()
    assert lock_unit.received_unlock_command(), "First unlock command should have been sent"

    # Simulate second credential arriving before first sequence completes
    lock_unit._received_unlock = False  # reset flag to detect a second command (test-only access)
    reader.send_valid_credential()

    # THEN: second request should be rejected — no second unlock command
    assert not lock_unit.received_unlock_command(), (
        "MCM sent a duplicate unlock command while sequence was in progress (REQ-007)"
    )


# ---------------------------------------------------------------------------
# TC-INT-008 — Out-of-order message
# ---------------------------------------------------------------------------

@pytest.mark.skip(
    reason="TC-INT-008: Requires MCM strict message-order enforcement — "
           "VirtualTopology does not validate message sequence. "
           "Implement once MCM enforces credential_event → unlock_command → "
           "lock_acknowledgement → door_opened_event ordering."
)
def test_out_of_order_message_rejected(virtual_topology, reader, lock_unit, door_sensor):
    # GIVEN: credential accepted, unlock_command sent
    virtual_topology.start()
    lock_unit.set_locked()
    reader.send_valid_credential()

    # WHEN: door_opened injected BEFORE lock_acknowledgement (reversed order)
    door_sensor.report_door_opened()   # out of order
    lock_unit.acknowledge_unlock()     # arrives late

    # THEN: MCM should reject the sequence; system stays locked
    # [ASSUMPTION: VirtualTopology would need message-order enforcement to emit this diagnostic]
    assert "COMM_SEQUENCE_ERROR" in virtual_topology.diagnostics
    assert lock_unit.is_locked


# ---------------------------------------------------------------------------
# TC-INT-009 — Node restart during unlock sequence
# ---------------------------------------------------------------------------

@pytest.mark.xfail(
    strict=True,
    reason="TC-INT-009: VirtualTopology does not detect reader.restart() or abort "
           "active unlock sequences on node disconnect. "
           "This test will pass once MCM disconnect detection is implemented."
)
def test_node_restart_during_unlock_aborts_sequence(virtual_topology, reader, lock_unit):
    # GIVEN: topology started but credential not yet processed by MCM
    virtual_topology.start()
    lock_unit.set_locked()
    reader._last_credential = "valid"  # credential registered (test-only: simulate in-progress state)

    # WHEN: reader restarts before MCM issues the unlock command
    reader.restart()

    # Attempt to trigger MCM processing after restart (stale credential should be ignored)
    reader.send_valid_credential()

    # THEN: no unlock command should be based on the pre-restart stale credential
    # [ASSUMPTION: MCM detects restart and does not process stale data]
    assert not lock_unit.received_unlock_command(), (
        "MCM sent unlock command after reader restart — stale credential was not discarded (REQ-009)"
    )
    assert lock_unit.is_locked
