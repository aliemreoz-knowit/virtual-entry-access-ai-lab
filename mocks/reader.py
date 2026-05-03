"""
Credential Reader mock for the virtualized entry/access-control lab.

This is a training scaffold — not a real hardware interface.
"""


class CredentialReader:
    """Simulates a credential reader node."""

    def __init__(self):
        self._last_credential = None
        self._available = True
        self._on_valid_credential = None  # callback wired by VirtualTopology
        self._on_invalid_credential = None  # callback wired by VirtualTopology

    def send_valid_credential(self):
        """Simulate presenting a valid credential."""
        self._last_credential = "valid"
        if self._on_valid_credential:
            self._on_valid_credential()

    def send_invalid_credential(self):
        """Simulate presenting an invalid credential."""
        self._last_credential = "invalid"
        if self._on_invalid_credential:
            self._on_invalid_credential()

    @property
    def last_credential(self):
        return self._last_credential

    def set_available(self):
        self._available = True

    def set_unavailable(self):
        self._available = False

    def restart(self):
        """Simulate a node restart."""
        self._last_credential = None
        self._available = True

    @property
    def is_available(self):
        return self._available
