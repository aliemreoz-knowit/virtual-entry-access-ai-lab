"""
Lock Unit mock for the virtualized entry/access-control lab.

This is a training scaffold — not a real hardware interface.
"""


class LockUnit:
    """Simulates a lock unit node."""

    def __init__(self):
        self._locked = True
        self._received_unlock = False
        self._acknowledged = False
        self._ack_delay_s = 0  # optional simulated delay for acknowledge_unlock()

    def set_locked(self):
        """Set the lock unit to locked state."""
        self._locked = True
        self._received_unlock = False
        self._acknowledged = False

    def set_unlocked(self):
        """Set the lock unit to unlocked state."""
        self._locked = False

    def received_unlock_command(self):
        """Check whether an unlock command was received."""
        return self._received_unlock

    def receive_unlock_command(self):
        """Simulate receiving an unlock command from the MCM."""
        self._received_unlock = True

    def acknowledge_unlock(self):
        """Simulate sending an acknowledgement back to the MCM."""
        if self._ack_delay_s > 0:
            import time
            time.sleep(self._ack_delay_s)
        self._acknowledged = True
        self._locked = False

    def set_ack_delay(self, delay_s):
        """Set a simulated delay (in seconds) for acknowledge_unlock()."""
        self._ack_delay_s = delay_s

    @property
    def is_locked(self):
        return self._locked

    @property
    def has_acknowledged(self):
        return self._acknowledged

    def restart(self):
        """Simulate a node restart."""
        self._locked = True
        self._received_unlock = False
        self._acknowledged = False
        self._ack_delay_s = 0
