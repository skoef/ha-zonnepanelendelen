# Home Assistant integration for zonnepanelendelen.nl

[Zonnepanelendelen](https://zonnepanelendelen.nl/) is an initiative to invest in solar projects. This integration allows you to display the produced energy of projects you invested in in you home assistant.

## Installation and configuration

Copy the `custom_components/zonnepanelendelen` folder to your `config/custom_components` folder and restart home assistant. You can now configure the integration.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=zonnepanelendelen)

## Known issues

- Currently, the integration only lists projects you invested in once during startup. When you invest in additional projects, you have to reload home assistant to add them.
