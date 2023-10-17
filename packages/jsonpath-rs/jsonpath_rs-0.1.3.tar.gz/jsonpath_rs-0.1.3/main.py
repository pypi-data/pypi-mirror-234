from jsonpath_rs import string_jsonpath_query

import json

# data = [{"book": "ali"}, {"book": "mammad"}]
data = {"data": [{"book": "ali"}, {"book": "mammad"}]}
j = json.dumps(data)
jp = "$.data[*]"
result = string_jsonpath_query(j, jp)
print(type(result))
print(result)