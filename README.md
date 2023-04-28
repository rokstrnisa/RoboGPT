# RoboGPT: A simple autonomous GPT-4 runner

[![](https://dcbadge.vercel.app/api/server/98KeRysd?style=flat)](https://discord.gg/98KeRysd)
[![Twitter Follow](https://img.shields.io/twitter/follow/rokstrnisa?style=social)](https://twitter.com/intent/follow?screen_name=rokstrnisa)

RoboGPT is a simple and extensible program that helps you run GPT-4 model autonomously. It is designed to be easy to understand, so that anyone can use it and extend it.

The program was inspired by [some of my earlier work](https://blog.rok.strnisa.com/2023/04/how-i-got-chatgpt-to-write-complete.html) and Auto-GPT.

**License**: This project is released under the [MIT License](LICENSE).

## Simple Demo

[![A simple demo of RoboGPT.](https://img.youtube.com/vi/mi0D4l7JRtQ/0.jpg)](https://www.youtube.com/watch?v=mi0D4l7JRtQ)

## Features

-   :robot: Simple and easy to understand codebase.
-   :wrench: Extensible design for easy contributions.
-   :arrows_counterclockwise: Continuous mode for ongoing interaction.
-   :speaker: Speech support (optional) for a more engaging user experience.

Planned:

-   :dizzy: Generic parsing and encapsulated action definitions.
-   :gear: Plug-in system for easy extensibility.

## Requirements

-   Python 3.10 or later.
-   OpenAI API key with access to [gpt-4 model](https://platform.openai.com/docs/models/gpt-4).
    At the time of writing, you need to join a waitlist, and OpenAI will give you access when capacity is available.
-   ElevenLabs key (optional for speech).

## Setup

-   Install [`pipenv`](https://pypi.org/project/pipenv/).
-   Clone this repo and change directory to it.
-   Run `pipenv shell` to enter the Python virtual environment and `pipenv install` to install the dependencies.
-   Rename `.env.template` to `.env` and fill in your [`OPENAI_API_KEY`](https://platform.openai.com/account/api-keys),
    and optionally [`ELEVEN_LABS_API_KEY`](https://elevenlabs.io) (for speech).

## Usage

Run `python robogpt/main.py` to start the program.

## Continuous Mode

The program does not run in continuous mode by default. To run it in continuous mode, simply use the command-line flag `--continuous`.

## Speech

On macOS, run `pip install PyObjC` to install the required dependency for speech.

To enable speech, use the command-line flag `--speech`.

## Sponsor

If you like this project, consider supporting its further development - [become a supporter](https://github.com/sponsors/rokstrnisa)!

Current Sponsors:

-   🥉 [Martin Köppelmann](https://github.com/koeppelmann)

## Contributing

Contributions to RoboGPT are very welcome! If you'd like to contribute, please follow these guidelines:

-   Submit issues for bugs or feature requests.
-   Create pull requests for proposed changes or new features. Make sure your changes are well-documented and follow the project's code style.
-   Join the community (see below) and participate in discussions to help shape the project's future.

## Community

Join [RoboGPT Discord server](https://discord.gg/98KeRysd) to get help, discuss ideas and collaborate.

To stay up-to-date, follow [@RokStrnisa](https://twitter.com/intent/follow?screen_name=rokstrnisa).
