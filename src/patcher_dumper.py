import os
import json
import sys

if len(sys.argv)>1 :
    filename = sys.argv [1]
else:
    filename = '.\\namedump.json'
if len(sys.argv)>2 :
    racename = sys.argv [2]
else:
    racename = 'wasphive'

patch_prefix = '[{"op": "add","path": "/'
patch_suffix = 'Description","value": "'
patch_postfix= '"}]'

dump_file = open(filename)
dump_obj  = json.load(dump_file)
dump_file.close()

for iterator in dump_obj:
    t_filepath = os.path.join(os.getcwd(),iterator['path'])
    print(t_filepath)
    os.makedirs(t_filepath,exist_ok = True)
    t_file = open(os.path.join(t_filepath,iterator['file']+'.patch'),'w')
    t_file.write(patch_prefix + racename + patch_suffix + iterator['desc'].replace('"','\\"') + patch_postfix)
    t_file.close()
