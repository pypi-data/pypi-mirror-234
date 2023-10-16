# ConcatMap

The `ConcatMap` module provides a class for abstract indexing of
concatenated, fixed-size entities.  Basically, it's a way to access many
things as if they were one thing.

## Installation

To install the module, run:

```
pip install concatmap
```

## Usage

```python
from concatmap import Concat

# Create a list of lists of integers
lsts = [list(range(n)) for n in range(1, 11)]

# Create a Concat object from the list of lists
c = Concat.from_arrays(*lsts)

# Access elements in the Concat object
element = c[50]

# Access slices in the Concat object
slice = c[50:100]

# iterate over the Concat object elements
for x in c:
  print(x)
```


## Testing

To run the unit tests for the module, run:

```
make ; make test
```

## License

This module is licensed under the MIT License.
