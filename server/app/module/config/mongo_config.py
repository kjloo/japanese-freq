class MongoConfig:
    def __init__(self, config: dict[str]):
        """
        Initialize the MongoConfig class.
        :param config: A dictionary containing the configuration.
        """

        # Load configuration from the YAML file
        self.host = config.get("mongo", {}).get("host")
        self.port = config.get("mongo", {}).get("port")
        self.db = config.get("mongo", {}).get("db")
        self.user = config.get("mongo", {}).get("user")
        self.password = config.get("mongo", {}).get("password")

    def get_server_url(self) -> str:
        """
        Get the server URL in the format "host:port".
        :return: The server URL.
        """
        return f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
