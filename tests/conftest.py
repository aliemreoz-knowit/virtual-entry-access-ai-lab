"""
Pytest fixtures for the virtualized entry/access-control lab.

These fixtures provide lightweight mock objects for testing.
They are intentionally simple — this is a training scaffold, not a real simulator.

The VirtualTopology wires the mocks together so that:
- A valid credential triggers the unlock command on the lock unit (if gateway is available).
- An invalid credential records a diagnostic event.
- Duplicate unlock requests during an active sequence are rejected.

Diagnostics are available via virtual_topology.diagnostics (list of string event names).
"""

import pytest

# Import mock classes from the mocks package
from mocks.reader import CredentialReader
from mocks.lock_unit import LockUnit
from mocks.door_sensor import DoorSensor
from mocks.gateway import Gateway


class VirtualTopology:
    """Minimal virtual topology coordinator for the lab.

    Wires the mock nodes together to simulate basic MCM behavior:
    valid credential → unlock command sent to lock unit (if gateway is available).
    invalid credential → diagnostic event recorded.
    """

    def __init__(self, reader, lock_unit, door_sensor, gateway):
        self._running = False
        self._reader = reader
        self._lock_unit = lock_unit
        self._door_sensor = door_sensor
        self._gateway = gateway
        self._diagnostics = []
        self._unlock_in_progress = False

    def start(self):
        self._running = True
        # Wire: when reader sends a valid credential, MCM sends unlock to lock unit
        self._reader._on_valid_credential = self._handle_valid_credential
        self._reader._on_invalid_credential = self._handle_invalid_credential

    def _handle_valid_credential(self):
        if self._running:
            if not self._gateway.is_available:
                self._diagnostics.append("GATEWAY_UNAVAILABLE")
                return
            if self._unlock_in_progress:
                return  # reject duplicate unlock request (REQ-007)
            self._unlock_in_progress = True
            self._lock_unit.receive_unlock_command()

    def _handle_invalid_credential(self):
        if self._running:
            self._diagnostics.append("INVALID_CREDENTIAL_REJECTED")

    def stop(self):
        self._running = False
        self._unlock_in_progress = False

    @property
    def diagnostics(self):
        """Return a copy of the diagnostics list."""
        return list(self._diagnostics)

    @property
    def is_running(self):
        return self._running


@pytest.fixture
def reader():
    """Provide a Credential Reader mock."""
    return CredentialReader()


@pytest.fixture
def lock_unit():
    """Provide a Lock Unit mock."""
    return LockUnit()


@pytest.fixture
def door_sensor():
    """Provide a Door Sensor mock."""
    return DoorSensor()


@pytest.fixture
def gateway():
    """Provide a Gateway mock."""
    return Gateway()


@pytest.fixture
def virtual_topology(reader, lock_unit, door_sensor, gateway):
    """Provide a virtual topology that wires the mock nodes together."""
    topo = VirtualTopology(reader, lock_unit, door_sensor, gateway)
    yield topo
    topo.stop()
