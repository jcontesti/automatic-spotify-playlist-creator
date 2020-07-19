import yaml


class ExtractionConfiguration:
    def __init__(
        self,
        configuration_file_path: str,
    ):
        self._yaml_configuration = self._read_yaml(configuration_file_path)

    @staticmethod
    def _read_yaml(yaml_file):
        with open(yaml_file, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def get_field(self, key: str):
        return self._yaml_configuration.get(key)

    def get_extractor_module_name(self):
        return self._yaml_configuration.get("extractor")[0].get("module_name")

    def get_extractor_class_name(self):
        return self._yaml_configuration.get("extractor")[0].get("class_name")
