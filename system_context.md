# Virtualized Entry / Access Control System — System Context

This document describes the system under test for the workshop lab.

> This is a training scaffold. All names, signals and APIs are generic placeholders.
> No real hardware, proprietary data or internal systems are referenced.

---

## Device Under Test (DUT)

**Main Control Module (MCM)** — the access controller.

The MCM receives credential events, validates them, sends unlock commands, monitors acknowledgements, tracks door state and raises diagnostics when something goes wrong.

---

## Mocked adjacent nodes

The following nodes are simulated in the virtual topology:

| Node | Role |
|------|------|
| **Credential Reader** | Reads and sends credential events (valid or invalid) to the MCM |
| **Lock Unit** | Receives unlock commands from the MCM and sends acknowledgements |
| **Door Sensor** | Reports door state (opened / closed) to the MCM |
| **Gateway** | Routes messages between network segments (CAN ↔ Ethernet) |

---

## Communication

| Protocol | Used for |
|----------|----------|
| CAN | Communication between MCM, Lock Unit and Door Sensor |
| Ethernet | Communication between MCM and Gateway; diagnostic reporting |

> Exact signal names, DBC file definitions and project-specific APIs are not available in this lab.
> Use generic placeholder names when referring to messages and signals.

---

## Environment

- **Virtual topology first** — all nodes run as software mocks in a virtual environment.
- **No physical hardware dependency** — the lab does not require access to real ECUs, CAN buses or vehicle hardware.
- **CI-ready** — tests are designed to run in a CI pipeline.
- **SIL/HIL migration path** — the same test scenarios can later be adapted for Software-in-the-Loop and Hardware-in-the-Loop environments.

---

## Testing goal

Validate the following behaviors **before physical hardware is available**:

- Nominal unlock flow (valid credential → unlock → door opened)
- Rejection of invalid credentials
- Timeout handling (lock unit, door sensor, diagnostic responses)
- Communication integrity (correct message order, no unexpected messages)
- Diagnostic reporting (correct diagnostic events raised on failure)
- Recovery behavior (system response when a mocked node restarts mid-sequence)

---

## Nominal unlock sequence

The expected message order for a successful unlock:

```
1. Credential Reader → MCM : credential_event (valid)
2. MCM → Lock Unit    : unlock_command
3. Lock Unit → MCM    : lock_acknowledgement
4. Door Sensor → MCM  : door_opened_event
```

If any step fails or times out, the MCM should raise appropriate diagnostics and keep the system in a safe (locked) state.
