**randog 0.14.0 — Randomly object generator**

**randog** is a package which helps to generate data randomly.

## Install

You can install from PyPI.

```shell
pip install -U randog
```

## Usage
For example:

```python
import uuid
import randog.factory

factory = randog.factory.from_example({"uuid": uuid.uuid4, "name": "", "age": 20})
generated = factory.next()

assert isinstance(generated, dict)
assert isinstance(generated["uuid"], uuid.UUID)
assert isinstance(generated["name"], str)
assert isinstance(generated["age"], int)
```

See the [documentation](https://unaguna.github.io/random-obj-generator/en/) for more details.


## Types that can be generated

- int, float, str, etc.
- [tuple](https://unaguna.github.io/random-obj-generator/en/doc.list_factory.html), [list](https://unaguna.github.io/random-obj-generator/en/doc.list_factory.html), [dict](https://unaguna.github.io/random-obj-generator/en/doc.dict_factory.html)
- datetime, date, time, timedelta
- (Experimental feature) [Model instance of SQLAlchemy](https://unaguna.github.io/random-obj-generator/en/doc.sqlalchemy.html)
