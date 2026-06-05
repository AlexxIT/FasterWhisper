import asyncio
import io
import logging
import os
import platform
import sys
from subprocess import PIPE, Popen

from homeassistant.core import HomeAssistant
from homeassistant.util import package

_LOGGER = logging.getLogger(__name__)

DOMAIN = "faster_whisper"


class Model:
    def __init__(self, hass: HomeAssistant, params: dict):
        from faster_whisper import WhisperModel

        self.model = WhisperModel(
            params["model"],
            cpu_threads=params.get("cpu_threads", 0),
            download_root=hass.config.path(DOMAIN),
            local_files_only=False,
        )
        self.lock = asyncio.Lock()
        self.beam_size = params.get("beam_size", 5)

    @property
    def supported_languages(self):
        return self.model.supported_languages

    async def transcribe(self, audio: bytes, language: str = None):
        async with self.lock:
            return self.model.transcribe(
                io.BytesIO(audio), language, beam_size=self.beam_size
            )


LIB_NAME = "faster_whisper==1.2.1"
WHEEL_URL = "https://github.com/AlexxIT/ctranslate2-alpine/releases/download/v4.7.2/ctranslate2-4.7.2-cp314-cp314-musllinux_1_2_{arch}.whl"


def install() -> bool:
    if package.is_installed(LIB_NAME):
        _LOGGER.debug("faster_whisper already installed")
        return True

    name, _ = platform.libc_ver()
    if name != "musl":
        _LOGGER.info("Install default faster_whisper")
        package.install_package(LIB_NAME)
        return True

    arch = platform.machine()
    if arch not in ("x86_64", "aarch64"):
        return False

    _LOGGER.info("Install faster_whisper for musl")

    # Install dependencies while ignoring `onnxruntime`:
    # https://github.com/SYSTRAN/faster-whisper/blob/master/requirements.txt
    ctranslate2 = WHEEL_URL.format(arch=arch)
    for name in (ctranslate2, "huggingface_hub>=0.23", "tokenizers>=0.13", "tqdm"):
        package.install_package(name)

    with Popen(
        [
            sys.executable,
            "-m",
            "uv",
            "pip",
            "install",
            "--quiet",
            "--no-deps",
            LIB_NAME,
        ],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        env=os.environ,
        close_fds=False,  # required for posix_spawn
    ) as process:
        _, stderr = process.communicate()
        if process.returncode != 0:
            _LOGGER.error(
                f"Can't install faster_whisper: %s",
                stderr.decode("utf-8").lstrip().strip(),
            )
            return False

    return True
