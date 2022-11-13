#!/usr/bin/python

import datetime
import json
import sys
import os
import shlex

# date = str(datetime.datetime.now())
# print(json.dumps({
#     "time": date
# }))

args_file = sys.argv[1]
args_data = open(args_file).read()

arguments = shlex.split(args_data)
for arg in arguments:
      if "=" in arg:
          
          (key, value) = arg.split("=")
          
          if key == "time":
              print("{}".format(value))
              rc = os.system("date -s \"%s\"" % value)
              
              if rc != 0:
                  print(json.dumps({
                      "failed": True,
                      "msg": "failed setting the time",
                      "value": -1
                  }))
                  sys.exit(1)
                  
              date = str(datetime.datetime.now())
              print(json.dumps({
                  "time": date,
                  "changed": True
              }))
              sys.exit(0)

date = str(datetime.datetime.now())
print(json.dumps({
    "time": date
}))