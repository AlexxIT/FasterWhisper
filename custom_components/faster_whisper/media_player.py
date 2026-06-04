from homeassistant.components import media_source
from homeassistant.components.media_player import (
    BrowseMedia,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType,
    async_process_play_media_url,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .utils import Model


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([FasterWhisperPlayer(config_entry)])


class FasterWhisperPlayer(MediaPlayerEntity):
    _attr_supported_features = (
        MediaPlayerEntityFeature.PLAY_MEDIA
        | MediaPlayerEntityFeature.SELECT_SOURCE
        | MediaPlayerEntityFeature.BROWSE_MEDIA
    )

    def __init__(self, config_entry: ConfigEntry) -> None:
        self.model: Model = config_entry.runtime_data

        self._attr_name = f"Faster Whisper Player"
        self._attr_unique_id = f"{config_entry.entry_id[:7]}-player"
        self._attr_state = MediaPlayerState.IDLE
        self._attr_source = "auto"
        self._attr_source_list = ["auto"] + self.model.supported_languages

    async def async_select_source(self, source: str) -> None:
        self._attr_source = source

    async def async_play_media(self, media_type: MediaType, media_id: str, **kwargs):
        if media_source.is_media_source_id(media_id):
            sourced_media = await media_source.async_resolve_media(
                self.hass, media_id, self.entity_id
            )
            media_id = async_process_play_media_url(self.hass, sourced_media.url)

        self._attr_state = MediaPlayerState.PLAYING
        self.async_write_ha_state()

        try:
            r = await async_get_clientsession(self.hass).get(media_id)
            data = await r.read()

            segments, info = await self.model.transcribe(data, self.source)

            self._attr_media_title = " ".join(i.text for i in segments).strip()
            self._attr_media_duration = info.duration
        except Exception as e:
            raise HomeAssistantError(e)
        finally:
            self._attr_state = MediaPlayerState.IDLE

    async def async_browse_media(
        self,
        media_content_type: str = None,
        media_content_id: str = None,
    ) -> BrowseMedia:
        return await media_source.async_browse_media(self.hass, media_content_id)
