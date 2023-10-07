import json

import fastjsonschema


class SciBecValidator:
    def __init__(self, schema_path: str) -> None:
        self.schema = self._load_schema(schema_path)
        self.device_schema = self.schema["components"]["schemas"]["Device"]
        self.device_validate = fastjsonschema.compile(self.device_schema)

    def _load_schema(self, schema_path) -> dict:
        with open(schema_path, "r", encoding="utf-8") as schema_file:
            content = schema_file.read()
            schema_content = json.loads(content)
        return schema_content

    def validate_device(self, device):
        self.device_validate(device)

    def validate_device_patch(self, config):
        properties = {k: v for k, v in self.device_schema["properties"].items() if k in config}
        schema = {"properties": properties, "required": []}
        fastjsonschema.validate(schema, config)
