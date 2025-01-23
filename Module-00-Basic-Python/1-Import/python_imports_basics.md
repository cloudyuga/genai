
### Key Differences Between `import xxx` and `from xxx import yyy`

| **Aspect**           | **import xxx**                          | **from xxx import yyy**                  |
|-----------------------|-----------------------------------------|------------------------------------------|
| **Scope of Import**   | Entire module                          | Specific function(s), class(es), or variable(s) |
| **Usage**             | Requires prefix (`xxx.`)               | Direct usage of imported item (`yyy`)    |
| **Memory Usage**      | May load the entire module              | Loads only the specified items           |
| **Conflict Handling** | No conflicts due to prefix              | Possible name conflicts without prefix   |




### Summary 

| Statement              | What It Does                                      | Usage Example           |
|------------------------|--------------------------------------------------|-------------------------|
| `import module`        | Imports the entire module with prefix            | `import math`           |
| `from module import item` | Imports specific item(s) from a module without needing a prefix | `from math import sqrt` |
| `import module as alias` | Imports a module with an alias to make it shorter to call | `import numpy as np`    |
