# HomeAssistant Automations for Brightness Control:

If you want to use the brightness control by turning the rotary encoder, you need to create two automations in HomeAssistant. The first one reads the brightness value from your ObsidianHub and sets a light entity's brightness. The second automation reads your light entity's brightness and sends it to your ObsidianHub.

## Instructions

1. Go to `Settings -> Automations & Scenes -> Create Automation`
2. Click the three dots (⋮) in top right -> `Edit in YAML`
3. Paste the following two automations (each in a seperately created automation). Make sure to replace `light.wled_main` with your light entity you want to control

## First Automation (ObsidianHub Brightness to your Light Entity)

Replace `light.wled_main` with the entity ID of your light (1 occurence).

```
description: "Sync ObsidianHub Brightness to Light Entity"
mode: single
triggers:
  - trigger: state
    entity_id:
      - number.obsidianhub_brightness_control
conditions: []
actions:
  - action: light.turn_on
    target:
      entity_id: light.wled_main
    data:
      brightness_pct: "{{ states('number.obsidianhub_brightness_control') | int }}"
```


## Second Automation (Reverse Sync your Light Entity to ObsidianHub))

Replace `light.wled_main` with the entity ID of your light (3 occurences).

```
description: "Sync Light Entity Brightness back to ObsidianHub"
mode: single
triggers:
  - trigger: state
    entity_id:
      - light.wled_main
    attribute: brightness
conditions:
  - condition: template
    value_template: >
      {% set wled_pct = ((state_attr('light.wled_main', 'brightness') |
      int(0)) / 255 * 100) | int %}
      {% set device = states('number.obsidianhub_brightness_control') | int(0) %}
      {{ (wled_pct - device) | abs > 3 }}
actions:
  - action: number.set_value
    target:
      entity_id: number.obsidianhub_brightness_control
    data:
      value: >
        {{ ((state_attr('light.wled_main', 'brightness') | int(0)) / 255 * 100) |
        int }}
```
