"""
Door Sensor mock for the virtualized entry/access-control lab.

This is a training scaffold — not a real hardware interface.
"""


class DoorSensor:
    """Simulates a door sensor node."""

    def __init__(self):
        self._door_opened = False
        self._available = True
        self._report_delay_s = 0  # optional simulated delay for report_door_opened()

    def report_door_opened(self):
        """Simulate the door sensor reporting that the door has opened."""
        if self._report_delay_s > 0:
            import time
            time.sleep(self._report_delay_s)
        self._door_opened = True

    def set_report_delay(self, delay_s):
        """Set a simulated delay (in seconds) for report_door_opened()."""
        self._report_delay_s = delay_s

    def report_door_closed(self):
        """Simulate the door sensor reporting that the door is closed."""
        self._door_opened = False

    def reported_door_opened(self):
        """Check whether door_opened has been reported."""
        return self._door_opened

    def set_available(self):
        self._available = True

    def set_unavailable(self):
        self._available = False

    def restart(self):
        """Simulate a node restart."""
        self._door_opened = False
        self._available = True
        self._report_delay_s = 0

    @property
    def is_available(self):
        return self._available
