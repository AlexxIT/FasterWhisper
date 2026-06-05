# Faster Whisper for Home Assistant

[Faster Whisper](https://github.com/SYSTRAN/faster-whisper) is a local Speech-to-Text engine. With [Home Assistant](https://www.home-assistant.io/), it allows you to create your own personal local voice assistant.

Typically, add-on users use the official version of [Whisper App](https://github.com/home-assistant/addons) from the Home Assistant core team. And that's right, because it runs in a separate Docker container and isn't limited by the Container version of Home Assistant.

Building a working version of the Faster Whisper dependencies for Alpine Linux (on which Home Assistant is based) was a real challenge. But I got it done - [ctranslate2-alpine](https://github.com/AlexxIT/ctranslate2-alpine).

## Warnings

Using such heavy software inside Home Assistant can cause performance and stability problems. Use with caution!

Large language models require a lot of RAM. Use with caution!

The models are downloaded to the Home Assistant config folder. They can greatly increase the size of your backups or sync with GitHub. Use with caution!

You have to delete unnecessary models yourself from the Home Assistant config folder.

## Installation

[![](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=AlexxIT&repository=FasterWhisper&category=Integration)

[HACS](https://hacs.xyz/) > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `AlexxIT/FasterWhisper`, Category: Integration > Add > wait > Faster Whisper > Install

Or manually copy `faster_whisper` folder from [latest release](https://github.com/AlexxIT/FasterWhisper/releases/latest) to `/config/custom_components` folder.

## Configuration

Settings > Integrations > Add Integration > Faster Whisper

You can setup multiple integrations with different models, and other settings. If you need to change settings, just delete the integration and set it up again.

Remember that each integration setup will consume a significant amount of RAM.

## Usage

You can use Speech-to-Text (STT) only inside [Assist pipeline](https://www.home-assistant.io/integrations/assist_pipeline/).

Settings > Voice assistants > Home Assistant > Select STT engine.

You can create several pipelines with different settings for different situations.

You can use [StreamAssist](https://github.com/AlexxIT/StreamAssist) custom component to convert almost [any camera](https://www.home-assistant.io/integrations/#camera) and almost [any speaker](https://www.home-assistant.io/integrations/#media-player) into a local [voice assistant](https://www.home-assistant.io/integrations/#voice).

You can try Home Assistant with local voice assistant on any PC with Windows using [HassWP](https://github.com/AlexxIT/HassWP) and this integration.
