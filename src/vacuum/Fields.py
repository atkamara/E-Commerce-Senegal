from .Model import Field
from itertools import product
from functools import lru_cache
import dateparser
from .Item import MainItem
from .Css import MainCss
from .utils import phone,currency,ravel,re
class CssField(Field,MainCss):
    css = [
        'xpaths',
        'relative_xpaths']
    def fmethod(self,value:str)->str:
        return ravel(value)
@MainItem.register
class ProductTitle(CssField):
    ...
@MainItem.register
class VendorLocation(CssField):
    ...
@MainItem.register
class PublishDate(CssField):
    def fmethod(self,value:str)->str:
        return dateparser.parse(ravel(value)).isoformat()
@MainItem.register
class Contact(CssField):
    def fmethod(self,value:str)->str:
        return re.sub('[\s\-\+]','',';'.join(set(re.findall(phone,ravel(value)))))
@MainItem.register
class PublishLink(CssField):
    def fmethod(self,value:str)->str:
        return ravel(value,sep=';')
@MainItem.register
class ProductPrice(CssField):
    def fmethod(self,value:str)->str:
        return re.sub('[\s,\.]','',';'.join(re.findall(currency,ravel(value,sep=';'))))
