# read_yaml_json_w1e6.py

import yaml
import json

with open("my_file_w1e6.yml") as f:
  my_list=yaml.load(f)
  print yaml.dump(my_list, default_flow_style=False)
with open("my_file_w1e6.json") as f:
  my_list=json.load(f)
  for element in my_list:
    print element

