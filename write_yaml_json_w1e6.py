# write_yaml_json_w1e6.py

import yaml
import json

my_list = [1,2,3,{'name':'fred','last':'flintstone','age':99}]
with open("my_file_w1e6.yml","w") as f:
  f.write(yaml.dump(my_list, default_flow_style=False))
with open("my_file_w1e6.json","w") as f:
  json.dump(my_list,f)
