# ObsidianHub Changelog

## v1.1.2 (WIP)

### New

- Update available notifications in HomeAssistant and MQTT with the ability to install firmware updates remotely from inside HomeAssistant
- Display a custom notification on your ObsidianHub: Send the notification over MQTT to show it on the display. You can specify the title, message and a timeout for how long the notification should be displayed (0 = show until rotary encoder pressed, or show for n seconds). You can also choose to display a border and/or show a button at the bottom of the notification

**MQTT topic:**

```
obsidianhub/notification
```

**Payload:**

```
{"title": "Info", "message": "This is an information with auto scrolling if the message is long (like this one)", "timeout": 10, "show_border": true, "show_button": true}
```

### Fixes & Improvements

- Enable auto sleep on firmware update available notification
- Renamed entities
- Changed entity icons
- Fixed auto dimming not working on certain pages
- Bug fixes

## v1.1.1

### New

- Auto-dim the display: You can enable auto dim to automatically dim the display in the dark when not actively using the device (pressing buttons)

### Fixes & Improvements

- Optimized intervals for location fetching to improve hangs after boot

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

## v1.0.4

- Initial release
