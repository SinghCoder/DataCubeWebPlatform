import xmlplain
import sys

# Read to plain object
with open(sys.argv[1]) as inf:
  root = xmlplain.xml_to_obj(inf, strip_space=True, fold_dict=True)

output = sys.argv[1][0:len(sys.argv[1])-4]+".yaml"

# Output plain YAML
with open(output, "w") as outf:
  xmlplain.obj_to_yaml(root, outf)