class AnkiConfig:
    def __init__(self, config: dict[str]):
        """
        Initialize the AnkiConfig class by loading configuration from a YAML file.

        :param config_file: Path to the YAML configuration file.
        """

        # Load configuration from the YAML file
        self.host = config.get("anki", {}).get("host")
        self.port = config.get("anki", {}).get("port")

    def get_server_url(self) -> str:
        """
        Get the Anki server URL.

        :return: The Anki server URL.
        """
        return f"{self.host}:{self.port}"
