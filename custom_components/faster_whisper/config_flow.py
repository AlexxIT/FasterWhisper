import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from wyoming_faster_whisper.const import WHISPER_LANGUAGES
from wyoming_faster_whisper.download import (
    FasterWhisperModel,
    find_model,
    download_model,
)

from . import DOMAIN

# medium model not exists https://github.com/rhasspy/models/releases
MODELS = [e.value for e in FasterWhisperModel if e != FasterWhisperModel.MEDIUM]


def find_or_download_model(model: str, model_path: str) -> bool:
    model = FasterWhisperModel(model)
    if find_model(model, model_path) is not None:
        return True

    return download_model(model, model_path) is not None


class ConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None, errors=None):
        if user_input:
            ok = await self.hass.loop.run_in_executor(
                None,
                find_or_download_model,
                user_input["model"],
                self.hass.config.path(DOMAIN),
            )
            if not ok:
                return await self.async_step_user(errors={"base": "download_model"})

            return self.async_create_entry(title="Faster Whisper", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("model", default="tiny-int8"): vol.In(MODELS),
                    vol.Required("language", default="en"): vol.In(WHISPER_LANGUAGES),
                    vol.Optional("beam_size", default=5): cv.port,
                    vol.Optional("cpu_threads", default=0): cv.positive_int,
                },
            ),
            errors=errors,
        )
