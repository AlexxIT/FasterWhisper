import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow

from .utils import DOMAIN

MODELS = [
    "rhasspy/faster-whisper-tiny-int8",
    "rhasspy/faster-whisper-base-int8",
    "rhasspy/faster-whisper-small-int8",
    "rhasspy/faster-whisper-medium-int8",
    "Systran/faster-whisper-tiny.en",
    "Systran/faster-whisper-tiny",
    "Systran/faster-whisper-base.en",
    "Systran/faster-whisper-base",
    "Systran/faster-whisper-small.en",
    "Systran/faster-whisper-small",
    "Systran/faster-whisper-medium.en",
    "Systran/faster-whisper-medium",
    "Systran/faster-whisper-large-v1",
    "Systran/faster-whisper-large-v2",
    "Systran/faster-whisper-large-v3",
    "Systran/faster-whisper-large-v3",
    "Systran/faster-distil-whisper-large-v2",
    "Systran/faster-distil-whisper-medium.en",
    "Systran/faster-distil-whisper-small.en",
    "Systran/faster-distil-whisper-large-v3",
    "distil-whisper/distil-large-v3.5-ct2",
    "mobiuslabsgmbh/faster-whisper-large-v3-turbo",
    "mobiuslabsgmbh/faster-whisper-large-v3-turbo",
]


class ConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None, errors=None):
        if user_input:
            return self.async_create_entry(title="Faster Whisper", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("model", default=MODELS[0]): vol.In(MODELS),
                    vol.Optional("beam_size", default=5): cv.positive_int,
                    vol.Optional("cpu_threads", default=0): cv.positive_int,
                },
            ),
            errors=errors,
        )
