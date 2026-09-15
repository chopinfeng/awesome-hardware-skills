---
name: esp32-ble-gatt
description: Build ESP-IDF 5.x firmware for ESP32-C3/S3 that exposes BLE GATT services with NimBLE — advertising, characteristic read/write/notify, MTU and connection parameter tuning. Use when the user asks for a BLE peripheral, GATT server, or "make the ESP32 show up in nRF Connect", including sensor-over-BLE and phone-app pairing flows.
---

# ESP32 BLE GATT (NimBLE)

This is a placeholder skill used to exercise the eval template. Replace with real content.

## When to use

- User wants an ESP32 to act as a BLE peripheral / GATT server.
- User mentions nRF Connect, LightBlue, GATT, characteristic, notify, advertising.

## Non-obvious rules

- ESP32-C3 has no Bluetooth Classic; do not pull in `esp_bt_gap_*`.
- With NimBLE, `CONFIG_BT_NIMBLE_ENABLED=y` must be set in `sdkconfig.defaults`, not just menuconfig, or CI builds drift.
- Notify payloads over 20 bytes silently truncate until MTU exchange completes; request MTU in `BLE_GAP_EVENT_CONNECT`.

## References

- `references/nimble-gatt-cheatsheet.md`
