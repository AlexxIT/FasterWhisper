from collections.abc import AsyncIterable

from homeassistant.components import stt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .utils import Model


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([FasterWhisperSTT(config_entry)])


class FasterWhisperSTT(stt.SpeechToTextEntity):
    def __init__(self, config_entry: ConfigEntry) -> None:
        self.model: Model = config_entry.runtime_data

        self._attr_name = "Faster Whisper"
        self._attr_unique_id = f"{config_entry.entry_id[:7]}-stt"

    @property
    def supported_languages(self) -> list[str]:
        return self.model.supported_languages

    @property
    def supported_formats(self) -> list[stt.AudioFormats]:
        return [stt.AudioFormats.WAV]

    @property
    def supported_codecs(self) -> list[stt.AudioCodecs]:
        return [stt.AudioCodecs.PCM]

    @property
    def supported_bit_rates(self) -> list[stt.AudioBitRates]:
        return [stt.AudioBitRates.BITRATE_16]

    @property
    def supported_sample_rates(self) -> list[stt.AudioSampleRates]:
        return [stt.AudioSampleRates.SAMPLERATE_16000]

    @property
    def supported_channels(self) -> list[stt.AudioChannels]:
        return [stt.AudioChannels.CHANNEL_MONO]

    async def async_process_audio_stream(
        self, metadata: stt.SpeechMetadata, stream: AsyncIterable[bytes]
    ) -> stt.SpeechResult:
        audio = b""
        async for chunk in stream:
            audio += chunk

        segments, _ = await self.model.transcribe(audio)
        text = " ".join(i.text for i in segments).strip()

        return stt.SpeechResult(text, stt.SpeechResultState.SUCCESS)
