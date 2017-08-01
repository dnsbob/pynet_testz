# read_yaml_json_w1e6.py

import yaml
import json
from pprint import pprint

with open("my_file_w1e6.yml") as f:
  my_list=yaml.load(f)
  print yaml.dump(my_list, default_flow_style=False)
  pprint(my_list)
with open("my_file_w1e6.json") as f:
  my_list=json.load(f)
  for element in my_list:
    print element
  pprint(my_list)
