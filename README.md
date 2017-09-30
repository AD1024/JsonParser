# JsonParser
A JSON Parser written in Python3

# Usage

## Simple Usage
- The major function is in `parser/Parser`.
```python
from parser.Parser import *
result = Parser(RAW_DATA).parse()
```

## Generate Tokens
Use `tokenizer/Tokenizer` and `tokenizer/Readers` to generate **Tokens**
```python
from tokenizer.Reader import *
from tokenizer.Tokenizer import *
from parser.Parser import *

reader r = Reader(RAW_DATA)
tokens = Tokenizer(r).getTokens()
tokenList = tokens.tokenList;

for i in tokenList :
    print(i.getType(), i.value)

result = Parser(tokenList).parse()
```

## Access enries
The method of accessing elements in `JSONArray` and `JSONObject` is the same as that of using native module(json).
```python
result = Parser(RAW_DATA).parse()
result[KEY] # For JSONObject
result[INDEX] # For JSONArray
```
Also, `JSONArray` supports foreach loop. 

# Issues
- Cannot deal with HTML tags(Tags will cause parser error)