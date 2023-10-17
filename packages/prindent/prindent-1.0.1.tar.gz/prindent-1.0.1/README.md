# prindent
Python module to print with automatic indentation

Sometimes it is useful to print with indentation to better visualize the data. This is particularly true when multiple `for` loops and `if` statements are nested. `prindent` can automatically indent everything for you.

### Usage

```python
from prindent import prindent

prindent('first loop')
for i in range(2):
    prindent('i:', i)
    prindent('second loop')
    for j in range(2):
        prindent('j:', j)
        if j == 1:
            prindent('j=1')

# first loop
#     i: 0
#     second loop
#         j: 0
#         j: 1
#             j=1
#     i: 1
#     second loop
#         j: 0
#         j: 1
#             j=1
```

`prindent` supports custom indentation strings:
```python
if True:
    if True:
        for i in range(2):
            prindent('Custom indent', indent='---> ')

# ---> ---> ---> Custom indent
# ---> ---> ---> Custom indent
```

`prindent` handles multiple lines:
```python
if True:
    prindent('String\nwith\nnewline')

#     String
#     with
#     newline
```

`prindent` accepts multiple `args` and `kwargs` just like `print()`:
```python
if True:
    prindent('first', 'second', end='$')

#     first second$
```
