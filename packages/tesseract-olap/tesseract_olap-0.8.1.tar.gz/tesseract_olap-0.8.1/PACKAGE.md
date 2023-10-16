<p>
<a href="https://github.com/Datawheel/tesseract-python/releases"><img src="https://flat.badgen.net/github/release/Datawheel/tesseract-python" /></a>
<a href="https://github.com/Datawheel/tesseract-python/blob/master/LICENSE"><img src="https://flat.badgen.net/github/license/Datawheel/tesseract-python" /></a>
<a href="https://github.com/Datawheel/tesseract-python/"><img src="https://flat.badgen.net/github/checks/Datawheel/tesseract-python" /></a>
<a href="https://github.com/Datawheel/tesseract-python/issues"><img src="https://flat.badgen.net/github/issues/Datawheel/tesseract-python" /></a>
</p>

## Installation

Besides the main contents of the package, you can install the optional dependencies for the backend driver of your choice:

* `tesseract-olap[clickhouse]`  
  Installs the dependency needed to enable the use of the `tesseract_olap.backend.clickhouse` module.

## Getting started

In its most basic form, the tesseract-olap package provides you with a way to translate OLAP-type queries into request statements that a data backend can understand and execute safely. The results obtained through the execution of server methods are python objects, and as such, can be used in any way the language allows.

```python
# example.py

import asyncio

from tesseract_olap.backend.clickhouse import ClickhouseBackend
from tesseract_olap import OlapServer

backend = ClickhouseBackend("clickhouse://user:pass@localhost:9000/database")
server = OlapServer(backend=backend, schema="./path/to/schema.xml")

async def get_data():
    query = DataRequest.new("cube_name", {
      "drilldowns": ["Time", "Country"],
      "measures": ["Units", "Duration"],
    })
    # `result` is an `AsyncIterable` which outputs tidy-data row dictionaries
    result = await server.execute(query)
    # you can handle the result with `async for`
    return tuple([item async for item in result])

if __name__ == "__main__":
    asyncio.run(get_data())
```

The server instance can then be used in other programs as the data provider, for simple (like data exploration) and complex (like data processing) operations.

---
&copy; 2022 [Datawheel, LLC.](https://www.datawheel.us/)  
This project is licensed under [MIT](./LICENSE).
