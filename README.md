# JsonParser
A JSON Parser written in Python3

# Usage

## Simple Usage
- The major function is in `parser/Parser`.
```python
from parser.Parser import *
result = Parser.parse(raw_data)
```

## Generate Tokens
Use `tokenizer/Tokenizer` and `tokenizer/Readers` to generate **Tokens**
```python
from tokenizer.Reader import *
from tokenizer.Tokenizer import *
from parser.Parser import *

reader r = Reader(raw_data)
tokens = Tokenizer(r).getTokens()
tokenList = tokens.tokenList

for i in tokenList :
    print(i.getType(), i.value)

result = Parser.parse(token_list)
```

## Access entries
The method of accessing elements in `JSONArray` and `JSONObject` is the same as that of using native module(json).
```python
result = Parser.parse(raw_data)
result[KEY] # For JSONObject
result[INDEX] # For JSONArray
```
Also, `JSONArray` supports foreach loop. 

## Get Python Data
The `JSONObject` and `JSONArray` support getting a python data `dict` and `list`.
```python
python_data = json_data.to_python()
```
or
```python
python_data = Parser.parse(raw_data, True)
```

# Issues
- Cannot deal with HTML tags(Tags will cause parser error)