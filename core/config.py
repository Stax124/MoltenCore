import json
import logging
import os
from io import TextIOWrapper
from typing import Optional, Union

from jsonschema import validate

from .exceptions import ValidatorNotFound


class Config:
    def __init__(
        self,
        config_path: str = "./config",
        validation_scheme_path: Optional[str] = None,
    ) -> None:
        logging.debug("Initializing config")

        self.path: str = config_path
        self.config_file: TextIOWrapper = self.create_config()
        self.config: dict = {}

        # Validation
        self.validation_scheme_path: Union[str, None] = validation_scheme_path
        self.validation_scheme = self._validator_from_file(validation_scheme_path)

        # Fallback
        self.fallback_file: Optional[TextIOWrapper] = self._load_fallback_file()
        self.fallback: Optional[dict] = self._load_fallback()

    def create_config(self) -> TextIOWrapper:
        if not os.path.exists(self.path):
            logging.debug("Config folder does not exist, creating")
            os.makedirs(self.path)

        if not os.path.exists(os.path.join(self.path, "/config.json")):
            logging.debug("Config file does not exist, creating")
            with open(os.path.join(self.path, "/config.json"), "w") as f:
                return f
        else:
            logging.debug("Config file exists, loading")
            with open(os.path.join(self.path, "/config.json"), "r") as f:
                return f

    def close_config(self) -> None:
        logging.debug("Closing config file")
        self.config_file.close()

    def _validator_from_file(self, validator_path: Optional[str]) -> Union[dict, None]:
        """Load a JSON schema from a file

        Args:
            validator_path (str): path to json schema file

        Raises:
            FileNotFoundError
        """

        logging.debug("Loading validation scheme from file")

        if not validator_path:
            logging.warning(
                "No validation scheme path given, config will not be validated"
            )
            return None

        with open(validator_path, "r") as f:
            return json.load(f)

    def _load_fallback_file(self) -> Union[TextIOWrapper, None]:
        if os.path.exists(os.path.join(self.path, "..", "fallback.json")):
            logging.debug("Fallback file exists, loading")

            with open(os.path.join(self.path, "..", "fallback.json"), "r") as f:
                return f
        else:
            logging.debug("Fallback file does not exist")

    def _load_fallback(self) -> Union[dict, None]:
        if self.fallback_file:
            logging.debug("Loading fallback dictionary from fallback file")
            return json.load(self.fallback_file)
        else:
            return None

    def validate_config(self):
        """Validate the config file against the validation scheme

        Raises:
            jsonschema.exceptions.ValidationError: The config file is not valid
            jsonschema.exceptions.SchemaError: The validation scheme is not valid
        """

        if self.validation_scheme:
            validate(self.config, self.validation_scheme)
        else:
            raise ValidatorNotFound("No validation scheme found")

    def __repr__(self) -> str:
        return str(self.config)
