# LDtk Python 

Load and parse LDtk files, with full types definitions. 

Automatically generated from Json Schema using QuickType.

See https://ldtk.io/api/

can be used like that:


```python 
import json
from ldtkpy.api import ldtk_json_from_dict

result = ldtk_json_from_dict(json.loads(json_string))
```