# MagicO - enabling attribute notation and JSONPath

`MagicO` (Magic Object) allows you to access a `dict`, `list`, or `tuple` Python object using the attribute notation or a JSONPath.

For example, given the following data object:


```python
my_data = {
    "a": 1,
    "b": {
        "c": 3,
        "d": (4, 5)
    },
    "e": [
        {"f": 6},
        "xyz",
    ],
}
```

to access attribute "f", you would need to use a series of subscripts, such as `my_data["e"][0]["f"])`.
As a programmer, you probably would find it more natural to use the attribute notation, such as `my_data.e[0].f`, or the JSONPath notation, such as `my_data["$.e[0].f"]`.
This is what `MagicO` enables you to do.

To install `MagicO`:

```bash
pip install magico
```

To use `MagicO`:

```python
from magico import MagicO

my_magic = MagicO(my_data)
```

## Attribute notation

To access an attribute using the attribute notation:

```python
print(my_magic) # Original data
# Output: {'a': 1, 'b': {'c': 3, 'd': (4, 5)}, 'e': [{'f': 6}, 'xyz']}

print(my_magic.e[0].f)
# Output: 6
```

You may create new attributes, change them, and delete them using the attribute notation.

```python
print(my_magic) # Original data
# Output: {'a': 1, 'b': {'c': 3, 'd': (4, 5)}, 'e': [{'f': 6}, 'xyz']}

my_magic.b.g = 7
print(my_magic) # b.g is created
# Output: {'a': 1, 'b': {'c': 3, 'd': (4, 5), 'g': 7}, 'e': [{'f': 6}, 'xyz']}

my_magic.b.g = 8
print(my_magic) # b.g is updated
# Output: {'a': 1, 'b': {'c': 3, 'd': (4, 5), 'g': 8}, 'e': [{'f': 6}, 'xyz']}

del my_magic.b.g
print(my_magic) # b.g is deleted
# Output: {'a': 1, 'b': {'c': 3, 'd': (4, 5)}, 'e': [{'f': 6}, 'xyz']}
```

## JSONPath notation

There are times when the attribute to access is programmatically formulated as a [JSONPath](https://github.com/json-path/JsonPath), such as "$.e[0].f".
In this case, you may use the JSONPath as a subscript to the `MagicO` object, as in the following example:

```python
print(my_magic) # Original data
# Output: {'a': 1, 'b': {'c': 3, 'd': (4, 5)}, 'e': [{'f': 6}, 'xyz']}

print(my_magic["$.e[0].f"])
# Output: 6

# The root element of the JSONPath can be omitted
print(my_magic["e[0].f"])
# Output: 6
```

With the `MagicO` subscript notation, you can create a "deep" attribute simply by assigning a value to it, and all missing parent attributes along the path will be created automatically. For example:

```python
my_magic["$.b.g.h.i"] = 9 # Creating a "deep" attribute b.g.h.i
print(my_magic) # Attribute "b" is added with "g.h" to get to "i"
# Output: {'a': 1, 'b': {'c': 3, 'd': (4, 5), 'g': {'h': {'i': 9}}}, 'e': [{'f': 6}, 'xyz']}

del my_magic["$.b.g"] # Deleting the parent will delete its tree
print(my_magic) # Attribute "b.g" is deleted
# Output: {'a': 1, 'b': {'c': 3, 'd': (4, 5)}, 'e': [{'f': 6}, 'xyz']}
```

## Data types

The data type `MagicO` returns depends on how you access it:

- Attribute notation:
  - `dict`, `list`, `tuple` and `MagicO` objects: Returns as a `MagicO` object
    - `.to_data()`: Returns the data
  - Scalar (`str`, `int`, `bool`, etc.): Returns the data
- JSONPath notation:
  - Returns the data

```python
print("MagicO object")
print(f"  {type(my_magic)}: {my_magic}") # <class 'magico.magico.MagicO'>: ...
print(f"  {type(my_magic.to_data())}: {my_magic.to_data()}") # <class 'dict'>: ...
print(f"  {type(my_magic.data_type())}: {my_magic.data_type()}") # <class 'type'>: <class 'dict'>

print("dict object")
print(f"  {type(my_magic.e[0])}: {my_magic.e[0]}") # <class 'magico.magico.MagicO'>: {'f': 6}
print(f"  {type(my_magic.e[0].to_data())}: {my_magic.e[0].to_data()}") # <class 'dict'>: {'f': 6}
print(f"  {type(my_magic.e[0].data_type())}: {my_magic.e[0].data_type()}") # <class 'type'>: <class 'dict'>

print("list object")
print(f"  {type(my_magic.e)}: {my_magic.e}") # <class 'magico.magico.MagicO'>: [{'f': 6}, 'xyz']
print(f"  {type(my_magic.e.to_data())}: {my_magic.e.to_data()}") # <class 'list'>: [{'f': 6}, 'xyz']
print(f"  {type(my_magic.e.data_type())}: {my_magic.e.data_type()}") # <class 'type'>: <class 'list'>

print("tuple object")
print(f"  {type(my_magic.b.d)}: {my_magic.b.d}") # <class 'magico.magico.MagicO'>: (4, 5)
print(f"  {type(my_magic.b.d.to_data())}: {my_magic.b.d.to_data()}") # <class 'tuple'>: (4, 5)
print(f"  {type(my_magic.b.d.data_type())}: {my_magic.b.d.data_type()}") # <class 'type'>: <class 'tuple'>

print("Scalar")
print(f"  {type(my_magic.e[0].f)}: {my_magic.e[0].f}") # <class 'int'>: 6

print("JSONPath access")
print(f"  {type(my_magic['$.e[0].f'])}: {my_magic['$.e[0].f']}") # <class 'int'>: 6
print(f"  {type(my_magic[''])}: {my_magic['']}") # <class 'dict'>: ...
```

`MagicO` supports all `dict`, `list`, and `tuple` behaviours: you may use [dict methods](https://www.w3schools.com/python/python_ref_dictionary.asp), [list methods](https://www.w3schools.com/python/python_ref_list.asp), and [tuple methods](https://www.w3schools.com/python/python_ref_tuple.asp) on a `MagicO` object, as if it is the underlying `dict`, `list`, or `tuple`.

For example,

```python
# Iterable
for m in my_magic:
    print(f"{m}: {my_magic[m]}")
# Output:
# a: 1
# b: {'c': 3, 'd': (4, 5)}
# e: [{'f': 6}, 'xyz']

# Sortable
my_magic.e.append([8, 6, 7, 5])
print(my_magic)
my_magic.e[-1].sort()
print(my_magic)
# Output:
# {'a': 1, 'b': {'c': 3, 'd': (4, 5)}, 'e': [{'f': 6}, 'xyz', [8, 6, 7, 5]]}
# {'a': 1, 'b': {'c': 3, 'd': (4, 5)}, 'e': [{'f': 6}, 'xyz', [5, 6, 7, 8]]}
```

## Referential pointers

Access to a `MagicO` object returns a pointer to the original data.
Updating the returned object will affect the original data object as well.
In short, `MagicO` is a wrapper of the original data you created it with.
They all share the same storage.

```python
print(my_data) # Original: {..., 'e': [{'f': 6}, 'xyz'], ...}
my_magic_data = my_magic.to_data()

# Update the data object
my_magic_data["e"][1] = "abc"
print(my_data) # Output: {..., 'e': [{'f': 6}, 'abc'], ...}

# Update the MagicO object
my_magic.e[1] = "xyz"
print(my_data) # Output: {..., 'e': [{'f': 6}, 'xyz'], ...}
```

Another example with JSONPath and delete. The deletion on the returned object `my_magic_attr` affects the original data `my_data`.

```python
my_magic_attr = my_magic["$.e"]
print(my_magic_attr) # Output: [{'f': 6}, 'xyz', [5, 6, 7, 8]]

del my_magic_attr[-1]
print(my_data) # Output: {'a': 1, 'b': {'c': 3, 'd': (4, 5)}, 'e': [{'f': 6}, 'xyz']}
```

---
Here is a [Jupyter version](https://github.com/jackyko8/magico/blob/main/tutorials/MagicO.ipynb) of this document.

If you have any questions or experience any issues, please log a [MagicO ticket on GitHub](https://github.com/jackyko8/magico/issues).
