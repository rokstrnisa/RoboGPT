# Robo-GPT: A simple autonomous GPT-4 runner

[![Twitter Follow](https://img.shields.io/twitter/follow/rokstrnisa?style=social)](https://twitter.com/intent/follow?screen_name=rokstrnisa)

Robo-GPT is a simple and extensible program that helps you run GPT-4 model autonomously. It is designed to be easy to understand, so that anyone can use it and extend it.

The program was inspired by some of my earlier research and Auto-GPT.

## Simple Demo

https://user-images.githubusercontent.com/241499/229651726-a441f569-44c9-4cc9-a128-dd1c386e2981.mov

## Features

The features are very limited at the moment, but more can be added easily.

## Requirements

-   Python 3.10 or later
-   OpenAI API key with access to GPT-4 API
-   ElevenLabs key (optional for speech)

## Setup

-   Install `pipenv`.
-   Clone this repo and change directory to it.
-   Run `pipenv install` to install the dependencies.
-   Rename `.env.template` to `.env` and fill in your [`OPENAI_API_KEY`](https://platform.openai.com/account/api-keys),
    and optionally [`ELEVEN_LABS_API_KEY`](https://elevenlabs.io) (for speech).

## Usage

Run `pipenv run python robo-gpt/main.py` to start the program.

## Continuous Mode

The program does not run in continuous mode by default. To run it in continuous mode, simply comment out the relevant lines in `main.py`.

## Contact

To share your thoughts or simply stay up-to-date, follow [@RokStrnisa](https://twitter.com/intent/follow?screen_name=rokstrnisa).
