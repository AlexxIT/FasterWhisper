# Faster Whisper for Home Assistant

[Faster Whisper](https://github.com/guillaumekln/faster-whisper) is a local Speech-to-Text engine. With [Home Assistant](https://www.home-assistant.io/), it allows you to create your own personal local voice assistant.

This is same code base as Home Assistant [Wisper Add-on](https://github.com/home-assistant/addons), developed by [@synesthesiam](https://github.com/synesthesiam) from [Nabu Casa](https://www.nabucasa.com/).

But packaged as Home Assistant custom integration. This can be useful when your environment does not allow you to install add-ons. For example, when your Home Assistant is running in **venv**, **Docker** or [Windows](https://github.com/AlexxIT/HassWP).

## Warnings

Using such heavy software inside Home Assistant can cause performance and stability problems. Use with caution!

Large language models require a lot of RAM. Use with caution!

The models are downloaded to the Home Assistant config folder. They can greatly increase the size of your backups or sync with GitHub. Use with caution!

You have to delete unnecessary models yourself from the Home Assistant config folder.

## Installation

[HACS](https://hacs.xyz/) > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `AlexxIT/FasterWhisper`, Category: Integration > Add > wait > Faster Whisper > Install

Or manually copy `faster_whisper` folder from [latest release](https://github.com/AlexxIT/FasterWhisper/releases/latest) to `/config/custom_components` folder.

## Configuration

Settings > Integrations > Add Integration > Faster Whisper

You can setup multiple integrations with different models, languages, and other settings. If you need to change settings, just delete the integration and set it up again.

Remember that each integration setup will consume a significant amount of RAM.

## Usage

You can use Speech-to-Text (STT) only inside [Assist pipeline](https://www.home-assistant.io/integrations/assist_pipeline/).

Settings > Voice assistants > Home Assistant > Select STT engine.

You can create several pipelines with different settings for different situations.

You can use [StreamAssist](https://github.com/AlexxIT/StreamAssist) custom component to convert almost [any camera](https://www.home-assistant.io/integrations/#camera) and almost [any speaker](https://www.home-assistant.io/integrations/#media-player) into a local [voice assistant](https://www.home-assistant.io/integrations/#voice).

You can try Home Assistant with local voice assistant on any PC with Windows using [HassWP](https://github.com/AlexxIT/HassWP) and this integration.
