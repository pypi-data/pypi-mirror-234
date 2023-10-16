import yaml
from pydantic import BaseModel, ValidationError


class EngineDBT(BaseModel):
    models_package: str


class Product(BaseModel):
    id: str
    version: str
    name: str
    description: str
    owner: str
    schedule: str
    engine: dict
    constraints: list


class DataProductSchema(BaseModel):
    schema_version: float
    product: Product


class YamlValidator:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_yaml(self) -> dict:
        with open(self.file_path, "r") as file:
            return yaml.safe_load(file)

    def validate_yaml(self, yaml_data: dict) -> DataProductSchema:
        try:
            dp_schema = DataProductSchema(**yaml_data)
            return dp_schema
        except ValidationError as e:
            print(f"Validation error: {e}")
            raise

    def validate_file(self) -> DataProductSchema:
        yaml_data = self.load_yaml()
        return self.validate_yaml(yaml_data)
