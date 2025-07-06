# Japanese Word Frequency

A Python project that utilizes MeCab to analyze a SRT file and return the frequency of the words.

## System Setup

Be sure to have MeCab installed on the machine where the code will be running.

### Mac

1. Install MeCab

```shell
brew install mecab
brew install mecab-ipadic
```

2. Install `git-lfs`

```shell
brew install git-lfs
git lfs install
```

## Setup Inputs and Ignorelist

1. Create an `input` directory in the base directory

```shell
mkdir -p input
```

2. Add a folder in the `input` directory and ensure there is a `.mp4` and a corresponding `.srt` file

```shell
mkdir -p input/anime
```

3. Copy `.ignorelist.example` into `.ignorelist.json` and add words you wish to ignore to the JSON list.

```shell
cat .ignorelist.example > .ignorelist.json
```

4. Copy `.env.example` into `.env` and update the settings

```shell
cp .env.example .env
```

## Run Server Locally

1. Install python 3.12

```shell
brew install python@3.12
```

2. Setup virtual python env

```shell
python3.12 -m venv .venv
source ./.venv/bin/activate
```

3. Install dependencies

```shell
pip install -r requirements.txt
python -m unidic download
```

4. Run program

```shell
make server-run
```

## Run Client Locally

1. Install dependencies

```shell
npm install --prefix client
```

2. Run client

```shell
make client-run
```

## Run with Docker

1. Use Make Commands

```shell
make setup
make build
make run
```
