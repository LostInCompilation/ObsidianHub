# ObsidianHub Changelog

## v1.2.0

### New

- Update available notifications in HomeAssistant and MQTT with the ability to install firmware updates remotely from inside HomeAssistant
- Display a custom notification on your ObsidianHub: Send the notification over MQTT to show it on the display. You can specify the title, message, and a timeout for how many seconds the notification should be displayed (0 = show until rotary encoder pressed, or show for n seconds). You can also choose to display a border and/or show a button with custom text at the bottom of the notification. The notification message will automatically scroll if it is too long and a smaller font will be selected automatically.
- Added automatic timezone detection

**MQTT topic:**

```
obsidianhub/notification
```

**Payload:**

```
{"title": "Info", "message": "This is an information with auto scrolling if the message is long (like this one)", "timeout": 0, "show_border": true, "button_text": true}
```

- `title`: The title of the notification. If left empty or missing, "Notification" will be used as the title
- `message`: The message of the notificstion. Must be specified.
- `timeout`: The time in seconds when to hide the notification again. Set to 0 to display it until rotary encoder is pressed.
- `show_border`: Show a border around the notification.
- `button_text`

### Fixes & Improvements

- Enable auto sleep on firmware update available notification
- Renamed entities
- Changed entity icons
- Fixed auto dimming not working on certain pages
- Improved IP location detection
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
