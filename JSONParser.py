from tokenizer.Readers import Reader
from tokenizer.Readers import PosReader
from tokenizer.Tokenizer import Tokenizer
from tokenizer.TokenList import *
from parser.Parser import Parser

r = Reader('{"1" : 2.00, "3" : [1,2,3,{"4" : "Alter"}]}')
t = Tokenizer(r).getTokens()
for i in t.tokenList :
    print(i.getType())

result = Parser('{"1" : 2.00, "3" : [1,2,3,{"4" : "Alter"}]}').parse()
print(result)
print(result['3'])
print(result['3'][3])
for i in result['3'] :
    print(i)

