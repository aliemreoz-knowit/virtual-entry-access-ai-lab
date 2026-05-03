# Unlock Flow Requirements

> These requirements are simplified for training purposes.
> Exact signal names, DBC definitions and project-specific APIs are not available.
> Use generic placeholder names where needed and mark assumptions clearly.

---

## REQ-001 — Nominal valid credential unlock

When a **valid credential** is presented by the Credential Reader, the Main Control Module (MCM) shall:

1. Validate the credential.
2. Send an unlock command to the Lock Unit.
3. Wait for the Lock Unit to acknowledge the unlock command.
4. Wait for the Door Sensor to report `door_opened`.
5. Complete the unlock flow without raising any diagnostic error.

**Timing constraint:** The full unlock sequence shall complete within **2000 ms** from credential event to door opened.

---

## REQ-002 — Invalid credential rejection

When an **invalid credential** is presented, the MCM shall:

1. Reject the unlock request.
2. **Not** send an unlock command to the Lock Unit.
3. Generate a diagnostic or audit event indicating the rejected credential.

---

## REQ-003 — Lock Unit timeout

If the Lock Unit does **not** acknowledge the unlock command within **300 ms**, the MCM shall:

1. Abort the unlock sequence.
2. Keep the system in a safe (locked) state.
3. Raise a `LOCK_UNIT_TIMEOUT` diagnostic event.

---

## REQ-004 — Delayed door sensor response

If the Door Sensor does **not** report `door_opened` within **500 ms** after the lock acknowledgement, the MCM shall:

1. Keep the system in a safe state.
2. Raise a `DOOR_SENSOR_TIMEOUT` diagnostic event.
3. Not retry the unlock automatically.

---

## REQ-005 — Gateway unavailable

If the Gateway is unavailable during unlock processing, the MCM shall:

1. Detect the communication failure.
2. Keep the system in a safe (locked) state.
3. Raise a `GATEWAY_UNAVAILABLE` diagnostic or communication error.
4. Not proceed with the unlock sequence.

---

## REQ-006 — Diagnostic response delay

The MCM shall respond to diagnostic requests within **1000 ms**.

If a diagnostic response exceeds this threshold, it shall be flagged as a timing violation in test results.

---

## REQ-007 — Repeated unlock request

If a new credential event arrives while an unlock sequence is already in progress, the MCM shall:

1. Reject the second request.
2. Continue processing the first unlock sequence.
3. Not send duplicate unlock commands to the Lock Unit.

---

## REQ-008 — Message received out of order

If the MCM receives messages in an unexpected order (e.g., `door_opened` before `lock_acknowledgement`), the MCM shall:

1. Reject the out-of-order sequence.
2. Keep the system in a safe state.
3. Raise a diagnostic event indicating a communication sequence error.

---

## REQ-009 — Mocked node restart during unlock sequence

If a mocked node (e.g., Credential Reader) restarts during an active unlock sequence, the MCM shall:

1. Detect the disconnection or restart.
2. Abort the current unlock sequence safely.
3. Not send unlock commands based on stale credential data.
4. Raise a diagnostic event indicating the node restart.

---

## Communication assumptions

The expected message order for a nominal unlock is:

```
1. credential_event (valid)
2. unlock_command
3. lock_acknowledgement
4. door_opened_event
```

> These are generic placeholder names.
> Exact signal names, message IDs and frame definitions depend on the project-specific DBC/API and are not available in this lab.
