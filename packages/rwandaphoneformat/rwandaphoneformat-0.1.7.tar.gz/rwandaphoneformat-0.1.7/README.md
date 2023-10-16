# rwandaphoneformat

rwandaphoneformat is a Python library for dealing with formtatting rwandan phone numbers.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) or [poetry](https://python-poetry.org/) to install rwandaphoneformat.

```bash
pip install rwandaphoneformat
```
or 
```bash
poetry add rwandaphoneformat
```

## Usage

```python
from rwandaphoneformat import in_250_format

# returns '250780000000'
in_250_format('0780000000')

# returns '250780000000'
in_250_format('+250780000000')

# returns '250780000000'
in_250_format('780000000')

# returns '250780000000'
in_250_format('250780000000')

# returns '1', here it returns the input, 
# if the input is not formatted as a Rwandan phone
in_250_format('1')
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)