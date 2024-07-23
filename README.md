# Japanese Word Frequency

A Python project that utilizes MeCab to analyze a SRT file and return the frequency of the words.

## System Setup

Be sure to have MeCab installed on the machine where the code will be running.

### Mac

```shell
brew install mecab
```

## Run Locally

1. Install python 3.11

```shell
brew install python@3.11
```

2. Install pipenv

```shell
pip install pipenv
```

3. Install dependencies

```shell
sudo apt-get install mecab libmecab-dev mecab-ipadic-utf8
pipenv install
```

5. Run program

```shell
pipenv run main -s res/example_sub.srt
```

## Run with Docker

1. Build docker

```shell
docker build -t japanese-freq .
```

2. Run docker compose

```shell
docker compose up
```
