from tokenizer.Readers import Reader
from tokenizer.Readers import PosReader
from tokenizer.Tokenizer import Tokenizer
from tokenizer.TokenList import *
from parser.Parser import Parser

r = Reader('{"1" : True, "3" : [1,2,3,{"4" : "Alter"}]}')
t = Tokenizer(r).getTokens()
for i in t.tokenList :
    print(i.getType())

result = Parser('{"1" : True, "3" : [1,2,3,{"4" : "Alter"}]}').parse()
print(result)
print(result['3'])
print(result['3'][3])
for i in result['3'] :
    print(i)

# # Example - 1
import urllib.request
request = urllib.request.Request('https://news-at.zhihu.com/api/4/news/latest') # Zhihu
resp = urllib.request.urlopen(request)
raw_data = resp.read()
data = raw_data.decode()
json_data = Parser(data).parse()
print(json_data)

# Example - 2
request = urllib.request.Request('http://local.shiyiquan.net/message/global/?time_update=0&Ajax=true') # Shiyiquan
resp = urllib.request.urlopen(request)
raw_data = resp.read().decode('unicode-escape')
json_data = Parser(raw_data).parse()
print(json_data)

