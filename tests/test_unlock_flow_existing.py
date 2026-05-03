"""
Existing smoke tests for the virtualized entry/access-control system.

These tests are intentionally incomplete.
They provide basic coverage for the unlock flow but are missing:
- timing assertions
- diagnostic event checks
- communication sequence verification
- negative scenario coverage (gateway unavailable, node restart, etc.)
- repeated unlock request handling

Use these tests as context when asking Cursor to generate better integration test cases.

NOTE: This is a training scaffold, not production test code.
"""


def test_valid_credential_unlock_smoke(virtual_topology, reader, lock_unit, door_sensor):
    """
    Smoke test: valid credential should trigger an unlock command.

    Missing coverage:
    - Does not assert timing (how fast the unlock happens)
    - Does not check that door_opened event is received
    - Does not verify diagnostic state after unlock
    - Does not check the full message sequence
    """
    # GIVEN: system is running and locked
    virtual_topology.start()
    lock_unit.set_locked()

    # WHEN: valid credential is presented
    reader.send_valid_credential()

    # THEN: lock unit should receive unlock command
    assert lock_unit.received_unlock_command()

    # TODO: assert door_sensor.reported_door_opened()
    # TODO: assert timing < 2000 ms
    # TODO: assert no diagnostic errors raised


def test_invalid_credential_does_not_unlock(virtual_topology, reader, lock_unit):
    """
    Smoke test: invalid credential should NOT trigger an unlock command.

    Missing coverage:
    - Does not check that a diagnostic/audit event was generated
    - Does not verify that the system remains locked
    - Does not test repeated invalid credential attempts
    """
    # GIVEN: system is running and locked
    virtual_topology.start()
    lock_unit.set_locked()

    # WHEN: invalid credential is presented
    reader.send_invalid_credential()

    # THEN: lock unit should NOT receive unlock command
    assert not lock_unit.received_unlock_command()

    # TODO: assert diagnostic_event raised for invalid credential
    # TODO: assert lock_unit remains locked


def test_unlock_with_gateway_available(virtual_topology, reader, lock_unit, gateway):
    """
    Smoke test: unlock should work when gateway is available.

    Missing coverage:
    - Does not test gateway unavailable scenario
    - Does not verify messages are routed through gateway
    - Does not check communication error handling
    """
    # GIVEN: system is running, gateway is available
    virtual_topology.start()
    lock_unit.set_locked()
    gateway.set_available()

    # WHEN: valid credential is presented
    reader.send_valid_credential()

    # THEN: unlock command should reach lock unit
    assert lock_unit.received_unlock_command()

    # TODO: test with gateway.set_unavailable()
    # TODO: assert GATEWAY_UNAVAILABLE diagnostic when gateway is down
