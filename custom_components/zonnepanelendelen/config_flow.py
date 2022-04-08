"""Config flow for zonnepanelendelen integration."""

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from .const import DOMAIN, PROJECTS_KEY
from . import _LOGGER
from .api import API, AuthenticationError

import voluptuous as vol


class ZPDConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example config flow."""

    def _show_user_form(self, errors=None):
        """Show the form to the user."""

        _LOGGER.debug("showing user form")
        data_schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def async_step_user(self, user_input=None):
        """Handle the start of the config flow."""
        if not user_input:
            _LOGGER.debug("user_info is not set yet")
            return self._show_user_form()

        # try to login with the credentials the user gave
        _LOGGER.debug("validating user input")
        try:
            zpd_client = API(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            await self.hass.async_add_executor_job(zpd_client.login)
        except AuthenticationError:
            _LOGGER.debug("authentication failed")
            return self._show_user_form({"base": "invalid_auth"})

        projects = await self.hass.async_add_executor_job(zpd_client.projects)
        if len(projects[PROJECTS_KEY]) == 0:
            return self.async_abort(reason="no_projects")

        _LOGGER.debug("storing user configuration")
        return self.async_create_entry(title=DOMAIN, data=user_input)
