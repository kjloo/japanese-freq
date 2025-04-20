class AnkiConfig:
    def __init__(self, config: dict[str]):
        """
        Initialize the AnkiConfig class by loading configuration from a YAML file.

        :param config_file: Path to the YAML configuration file.
        """
        self.url = "http://localhost"  # Default value
        self.port = "8765"  # Default value

        # Load configuration from the YAML file
        self.url = config.get("anki", {}).get(
            "url", self.url)
        self.port = config.get("anki", {}).get("port", self.port)

    def get_server_url(self) -> str:
        """
        Get the Anki server URL.

        :return: The Anki server URL.
        """
        return f"{self.url}:{self.port}"
