import yaml
from jsonschema import validate
import json

with open('log.yml', 'r') as f:
    y = yaml.safe_load(f)

with open("cg.schema","r") as f:
    s = f.read() 
    schema = json.loads(s)

validate(instance=y,schema=schema)