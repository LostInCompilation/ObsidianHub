# ObsidianHub - Changelog

## v1.2.1

### New

- xxxxxx

### Fixes & Improvements

- Location will be fetched periodically, instead of once at boot-up

---

## v1.2.0

### New

- Added automatic timezone detection
- Added total device-on-time counter
- Run firmware update directly from inside HomeAssistant: New update available notifications in HomeAssistant and MQTT with the ability to install firmware updates remotely from inside HomeAssistant
- Display a custom notification on your ObsidianHub: Send the notification over MQTT to show it on the display. You can specify the `title`, `message`, and a `timeout` for how many seconds the notification should be displayed (0 = show until rotary encoder pressed, or show for N seconds). You can also choose to display a border and/or show a button with custom text at the bottom of the notification. The notification message will automatically scroll if it is too long and a smaller font will be selected automatically to fit more text.

**MQTT topic:**

The ObsidianHub is subscribed to

```txt
obsidianhub/notification
```

**Payload:**

```json
{
    "title": "INFO",
    "message": "This is an information with auto scrolling if the message is long (like this one)",
    "timeout": 0,
    "show_border": false,
    "button_text": "OK"
}
```

- `title`: The title of the notification. If left empty or missing, "INFO" will be used as the default title
- `message` (required): The message of the notificstion. Must be specified or notification will be ignored
- `timeout`: The time in seconds when to hide the notification again. Set to 0 to display it until rotary encoder is pressed. Default: `0`
- `show_border`: Show a border around the notification. Default: `false`
- `button_text`: The text of the button. Leave empty to hide the button. Default: No button

If an optional parameter is missing, it's default value will be used.

### Fixes & Improvements

- Enable auto sleep on firmware update available notification
- Fixed auto dimming not working on certain pages
- Improved IP location detection
- Weather now updates much faster after boot
- Fixed display flickering at power on
- Renamed entities
- Changed entity icons
- Many backend optimizations
- Bug fixes

---

## v1.1.1

### New

- Auto-dim the display: You can enable auto dim to automatically dim the display in the dark when not actively using the device (pressing buttons)

### Fixes & Improvements

- Optimized intervals for location fetching to improve hangs after boot

---

## v1.1.0

### New

- Weather dashboard with automatic location detection
- `Later`-button for firmware updates, allowing you to postpone installation of the update
- Select which components should go to sleep (Display, LEDs or both)

### Fixes & Improvements

- LED and display fade-out synchronization issue
- Display flickering when rebooting
- Extended flash write intervals to reduce wear
- Various minor enhancements and bug fixes

---

## v1.0.4

- Initial release
