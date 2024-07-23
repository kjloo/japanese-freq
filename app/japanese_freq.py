import MeCab

wakati = MeCab.Tagger("-Owakati")


def main():
    print(wakati.parse("pythonが大好きです").split())


if __name__ == "__main__":
    input_file: str = 'input/sub.srt'
    output_dir: str = 'output'
    main()
