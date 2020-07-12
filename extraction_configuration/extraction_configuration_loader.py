import glob
import yaml
from extraction_configuration.extraction_configuration import ExtractionConfiguration


class ExtractionConfigurationLoader:
    EXTRACTION_CONFIGURATION_FILES_PATH = "examples/*.yaml"

    def __init__(
        self,
    ):
        self._configuration_files = glob.glob(self.EXTRACTION_CONFIGURATION_FILES_PATH)

    @staticmethod
    def _read_yaml(yaml_file):
        with open(yaml_file, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def return_configuration_files(self) -> [ExtractionConfiguration]:
        for configuration_file in self._configuration_files:
            yield ExtractionConfiguration(self._read_yaml(configuration_file))
