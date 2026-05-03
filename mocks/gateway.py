"""
Gateway mock for the virtualized entry/access-control lab.

This is a training scaffold — not a real hardware interface.
"""


class Gateway:
    """Simulates a gateway node that routes messages between CAN and Ethernet."""

    def __init__(self):
        self._available = True
        self._messages_routed = 0

    def set_available(self):
        """Set the gateway to available state."""
        self._available = True

    def set_unavailable(self):
        """Set the gateway to unavailable state (simulate network failure)."""
        self._available = False

    @property
    def is_available(self):
        return self._available

    def route_message(self):
        """Simulate routing a message through the gateway."""
        if self._available:
            self._messages_routed += 1
            return True
        return False

    @property
    def messages_routed(self):
        return self._messages_routed

    def restart(self):
        """Simulate a node restart."""
        self._available = True
        self._messages_routed = 0
