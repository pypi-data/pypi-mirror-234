from dataclasses import dataclass, field

import yaml
from marshmallow import Schema, ValidationError


@dataclass(frozen = True)
class TypeDesc:
    """
    Type descriptor: schema, example, etc.
    """

    dict_schema: Schema = field()
    ref_name: str = field()
    dict_example: dict = field()
    default_file_path: str = field()

    def from_default_file(self):
        return self.from_yaml_file(self.default_file_path)

    def from_yaml_file(self, file_path: str):
        with open(file_path) as yaml_file:
            yaml_data = yaml_file.read()
        return self.from_input_dict(yaml.safe_load(yaml_data))

    def from_yaml_str(self, yaml_str: str):
        return self.from_input_dict(yaml.safe_load(yaml_str))

    def from_input_dict(self, input_dict: dict):
        return self.dict_schema.load(input_dict)

    def validate_dict(self, input_dict: dict):
        validation_errors = self.dict_schema.validate(input_dict)
        if validation_errors:
            raise ValidationError(validation_errors)
