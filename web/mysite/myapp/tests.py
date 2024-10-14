from django.test import TestCase

import json

# Your JSON string
json_string = '["\\u0e40\\u0e04\\u0e23\\u0e37\\u0e48\\u0e2d\\u0e07\\u0e43\\u0e0a\\u0e49\\u0e44\\u0e1f\\u0e1f\\u0e49\\u0e32", "\\u0e40\\u0e2a\\u0e37\\u0e49\\u0e2d\\u0e1c\\u0e49\\u0e32"]'

# Decode the JSON
preferences = json.loads(json_string)

# Print the decoded preferences
for preference in preferences:
    print(preference)
