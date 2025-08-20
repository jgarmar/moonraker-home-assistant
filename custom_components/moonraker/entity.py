"""Base class entity for Moonraker."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CONF_OPTION_DISABLE_SWITCH


class BaseMoonrakerEntity(CoordinatorEntity):
    """Base class entity for Moonraker."""

    def __init__(self, coordinator, config_entry):
        """Init."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.api_device_name = coordinator.api_device_name

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not super().available:
            return False

        # Check if integration is disabled by switch
        disable_switch_entity_id = self.config_entry.options.get(CONF_OPTION_DISABLE_SWITCH)

        if not disable_switch_entity_id:
            # No disable switch configured, use default availability
            return True

        try:
            # Get the state of the disable switch
            switch_state = self.hass.states.get(disable_switch_entity_id)
            if switch_state is None:
                # Entity doesn't exist, assume available
                return True

            # If switch is 'off', entity should be unavailable
            return switch_state.state != "off"
        except Exception:
            # In case of any error, assume available
            return True

    @property
    def device_info(self):
        """Entity device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_entry.entry_id)},
            name=self.api_device_name,
            model=DOMAIN,
            manufacturer=DOMAIN,
        )
