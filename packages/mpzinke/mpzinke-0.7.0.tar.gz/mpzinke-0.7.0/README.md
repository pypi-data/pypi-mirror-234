# Python
Python libraries for MPZinke.

## Modules

### `DownloadIterator`
An object that takes a request to download large amounts of data and can run a function for each chunk.

#### Alternatives & Justification
`requests` allows for downloading large amounts of data, but when downloading a large amount of data, memory usage can be a factor. As such, writing to a file may be required. The DownloadIterator object wraps the request to allow for iterative download and processing of data.

Additionally, the request timeout specifies the amount of time for the server to respond, not the amount of time spent downloading the response. DownloadIterator provides a way to specify a maximum amount of time downloading a file.

#### Usage
[Usage can be found here](./Examples/DownloadIterator.py)
**Notably, `stream` must be set to `True`.**


### `Generic`
A class that can be called or inherited to make a function, method or class generic.

#### Alternatives & Justification
`typing.Generic` is a built-in class for generics. It however lacks the ability to be inherited from nor to store the generic's type. EG, if `MyGenericClass` inherits from `typing.Generic`, there is no way in `MyGenericClass[int]` to know the type of int once the class is instantiated.

Further more, `typing.Generic` cannot be applied to functions. As such, the `mpzinke.Generic` stores the type in a `.__args__` attribute like `list` and `Dict`.

#### Usage
[Usage can be found here]()


### `is_json(string: str) -> bool:`
`is_json` checks when a string is JSON parsable.

#### Alternatives & Justification
`json.loads` is the core of the `is_json` function. However to know if a string can be safely parsed, one must wrap it with a try-catch block. This does that automatically.

#### Usage
[Usage can be found here](./Examples/is_json.py)

#### Possible Future Enhancements
1. Add optional function to execute if string is successfully parsed.


### `Server`
`Server` is a class that wraps a Flask server to provide for easier server setup, error handling, authorization, and route addition. Additionally, it uses the doc strings of functions' passed to routes to document all endpoints.

#### Alternatives & Justification
Flask servers offer great API's for adding routes, but are limited in that a route only take 1 function for all METHODS. 

#### Usage
[Usage can be found here](./Examples/Generic.py)

#### Possible Future Enhancements
1. Add optional function to execute if string is successfully parsed.



A Flask server class for simple routing by HTTP method.




## Build Commands
FROM: https://packaging.python.org/en/latest/tutorials/packaging-projects/

- `python3 -m pip install --upgrade build`
- `python3 -m pip install --upgrade twine`
- `python3 -m build`
- `python3 -m twine upload --repository testpypi dist/*`
	- username: `__token__`
	- password: `<API KEY>`

`python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps python_server_MPZinke`
