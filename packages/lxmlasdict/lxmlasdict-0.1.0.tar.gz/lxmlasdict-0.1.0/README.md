# lxmlasdict

`lxmlasdict` is just wrapper that allows you to treat lxml tree elements as if you were working with a dict. elements are searched only when accessing keys

```sh
pip install lxmlasdict
```

##

There are a few things to remember when working with this wrapper:
- the wrapper returns None only when accessing the keys "#text" and "@attr" if they do not exist, because they are final elements that have no children.
- the wrapper does not return None when accessing other keys that do not exist; instead, it returns an empty wrapper that can be checked for the None value or its length

## Examples

```py
>>> data = lxmlasdict.from_string("""
...     <root a="testa">
...         <child>
...             <item>text 1</item>
...             <item>text 2</item>
...         </child>
...         <example b="testb">
...             example text
...         </example>
...         <test-ns:example xmlns:test-ns="http://test-ns.com/">
...             example text (namespaced)
...         </test-ns:example>
...     </root>
... """)
```

#### Accessing to only one element

```py
>>> print(data['child']['item']['#text'])
elements
```

#### Accessing to multiple elements

```py
>>> for item in data['child']['item']:
...     print(item['#text'])
... 
elements
more elements
```

#### Checking for element presence

```py
>>> if data['child']['item']:
...     print('element exists')
... else:
...     print('element does not exist')
... 
element exists

>>> if data['child']['test']:
...     print('element exists')
... else:
...     print('element does not exist')
... 
element does not exist
```

#### Counting the number of elements

```py
>>> print(len(data['child']['item']))
2
```

### Accessing attributes

```py
>>> print(data['@a'])
testa

>>> print(data['example']['@b'])
testb
```

### Accessing to elements with namespace

```py
>>> print(data['test-ns:example']['#text'])
example text (namespaced)
```


### Convert element and its contents to dict

```py
>>> data = lxmlasdict.to_dict(data)
>>> print(json.dumps(data, indent=4))
{
    "root": {
        "child": {
            "item": [
                "text 1",
                "text 2"
            ]
        },
        "example": {
            "@b": "testb",
            "#text": "example text"
        },
        "test-ns:example": "example text (namespaced)",
        "@a": "testa"
    }
}
```
