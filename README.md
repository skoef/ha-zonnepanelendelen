# Home Assistant integration for zonnepanelendelen.nl

[Zonnepanelendelen](https://zonnepanelendelen.nl/) is an initiative to invest in solar projects. This integration allows you to display the produced energy of projects you invested in in you home assistant.

## Installation and configuration

- Copy the `custom_components/zonnepanelendelen` folder to your `custom_components` folder.
- Add something similar to this in your `configuration.yaml`:

```yaml
sensor:
  - platform: zonnepanelendelen
    # replace with your credentials
    username: john@doe.com
    password: s3cr3t
```

- Restart home assistant
- You should be able to see a Zonnepanelendelen entity per project you invested in.

## Known issues

- Currently, the integration only lists projects you invested in once during startup. When you invest in additional projects, you have to reload home assistant to add them.
