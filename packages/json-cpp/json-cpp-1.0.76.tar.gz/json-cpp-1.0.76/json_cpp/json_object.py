import json
from .util import check_type
from datetime import datetime
import requests
from os import path


def json_parameters_function():
    def inner(func):
        def wrapper(json_object):
            if type(json_object) is str:
                json_object = JsonObject.load(json_object)
            p = {}
            for v in func.__code__.co_varnames:
                if v in json_object.__dict__:
                    p[v] = json_object.__dict__[v]
                else:
                    p[v] = None
            return func(**p)
        return wrapper
    return inner


class classorinstancemethod(classmethod):

    def __get__(self, instance, type_):
        descr_get = super().__get__ if instance is None else self.__func__.__get__
        return descr_get(instance, type_)


class JsonDate:
    date_format = '%Y-%m-%d %H:%M:%S.%f'


class JsonObject:

    def __init__(self, **kwargs):
        if type(self) is JsonObject:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __str__(self):
        s = ""
        for k in self.get_members():
            if k[0] == "_":
                continue
            if s:
                s += ","
            s += "\"%s\":" % k
            i = self[k]
            if isinstance(i, str):
                s += "%s" % json.dumps(i)
            elif isinstance(i, datetime):
                s += "\"%s\"" % i.strftime(JsonDate.date_format)
            elif isinstance(i, bool):
                s += "%s" % str(i).lower()
            else:
                s += "%s" % str(i)
        return "{%s}" % s


    def get_numeric_values(self):
        values = JsonList()
        for k in self.get_numeric_columns():
            values.append(self[k])
        return values

    def get_values(self):
        values = JsonList()
        for k in self.get_columns():
            values.append(self[k])
        return values

    def get_numeric_columns(self):
        columns = JsonList(list_type=str)
        for v in self.get_members():
            if isinstance(self[v], JsonObject):
                columns += [v + "." + c for c in self[v].get_numeric_columns()]
            else:
                i = self[v]
                t = type(i)
                if t is float or t is int or t is bool:
                    columns.append(v)
        return columns

    def into(self, cls: type):
        if not issubclass(cls, JsonObject):
            raise RuntimeError("type must derive from JsonObject")
        nv = cls()
        for c in self.get_columns():
            nv[c] = self[c]
        return nv

    def get_columns(self):
        columns = JsonList(list_type=str)
        for v in self.get_members():
            if isinstance(self[v], JsonObject):
                columns += [v + "." + c for c in self[v].get_columns()]
            else:
                columns.append(v)
        return columns

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        for k in self.get_members():
            if self[k] != other[k]:
                return False
        return True

    def __getitem__(self, key):
        if "." in key:
            parts = key.split(".")
            new_key = ".".join(parts[1:])
            key = parts[0]
            return self[key][new_key]
        else:
            return getattr(self, key)

    def __setitem__(self, key, value):
        if "." in key:
            parts = key.split(".")
            new_key = ".".join(parts[1:])
            key = parts[0]
            self[key][new_key] = value
        else:
            setattr(self, key, value)

    def __iter__(self):
        for k in self.get_members():
            yield k

    def get_members(self):
        members = []
        v = vars(self)
        for k in v:
            if k[0] == "_":
                continue
            members.append(k)
        return members

    def copy(self):
        return self.__class__.parse(str(self))

    def format(self, format_string: str):
        for k in self.get_members():
            if not isinstance(self[k], JsonObject):
                continue
            pos = format_string.find("{"+k+":")
            if pos >= 0:
                sub_format_start = format_string.find(":", pos) + 1
                sub_format_end = sub_format_start
                bracket_count = 1
                while bracket_count and sub_format_end < len(format_string):
                    c = format_string[sub_format_end]
                    if c == '{':
                        bracket_count += 1
                    if c == '}':
                        bracket_count -= 1
                    sub_format_end += 1
                sub_format = format_string[sub_format_start:sub_format_end-1]
                sub_str = self[k].format(sub_format)
                format_string = format_string[:pos] + sub_str + format_string[sub_format_end:]
        return format_string.format(**vars(self))

    @classorinstancemethod
    def parse(cls_or_self, json_string: str = "", json_dictionary: dict = None):
        if json_string:
            json_dictionary = json.loads(json_string)

        if type(cls_or_self) is type:
            new_object = cls_or_self()
        else:
            new_object = cls_or_self

        for key in json_dictionary:
            member = getattr(new_object, key)
            it = type(member)
            if issubclass(it, JsonObject):
                av = it.parse(json_dictionary=json_dictionary[key])
                setattr(new_object, key, av)
            elif issubclass(it, JsonList):
                member.parse(json_list=json_dictionary[key])
            elif it is datetime:
                av = datetime.strptime(json_dictionary[key], JsonDate.date_format)
                setattr(new_object, key, av)
            else:
                av = it(json_dictionary[key])
                setattr(new_object, key, av)
        return new_object

    @staticmethod
    def load(json_string: str = "", json_dictionary_or_list=None):
        if json_string:
            check_type(json_string, str, "wrong type for json_string")
            json_dictionary_or_list = json.loads(json_string)
        if isinstance(json_dictionary_or_list, list):
            new_list = JsonList(list_type=None)
            for item in json_dictionary_or_list:
                if isinstance(item, list) or isinstance(item, dict):
                    new_item = JsonObject.load(json_dictionary_or_list=item)
                else:
                    new_item = item
                new_list.append(new_item)
            return new_list
        elif isinstance(json_dictionary_or_list, dict):
            new_object = JsonObject()
            for key in json_dictionary_or_list.keys():
                if isinstance(json_dictionary_or_list[key], dict) or isinstance(json_dictionary_or_list[key], list):
                    setattr(new_object, key, JsonObject.load(json_dictionary_or_list=json_dictionary_or_list[key]))
                else:
                    setattr(new_object, key, json_dictionary_or_list[key])
            return new_object
        else:
            raise TypeError("wrong type for json_dictionary_or_list")

    def save(self, file_path: str):
        with open(file_path, 'w') as f:
            f.write(str(self))

    @classmethod
    def load_from_file(cls, file_path: str):
        if not path.exists(file_path):
            return None
        json_content = ""
        with open(file_path) as f:
            json_content = f.read()
        if cls is JsonObject:
            return cls.load(json_content)
        else:
            return cls.parse(json_content)

    @classmethod
    def load_from_url(cls, uri: str):
        req = requests.get(uri)
        if req.status_code == 200:
            if cls is JsonObject:
                return cls.load(req.text)
            else:
                return cls.parse(req.text)
        return None

    def __dataframe_values__(self):
        return [v.to_dataseries(recursive=True) if isinstance(v, JsonObject) else v.to_dataframe(recursive=True) if isinstance(v, JsonList) else v for v in self.get_values()]

    def to_dataseries(self, recursive: bool = False):
        import pandas as pd
        columns = self.get_columns()
        if recursive:
            values = self.__dataframe_values__()
        else:
            values = self.get_values()

        return pd.core.series.Series(dict(zip(columns,values)))


class SortOrder:
    Ascending = 0
    Descending = 1


class SearchType:
    Aprox = 0
    Exact = 1


class NotFoundBehavior:
    RaiseError = 0
    ReturnNone = 1


def bin_search(l, v, order=SortOrder.Ascending, search_type=SearchType.Aprox, key=None, not_found_behavior=NotFoundBehavior.RaiseError):
    lo = 0
    hi = len(l) - 1
    mi = int((hi + lo) / 2)
    if order == SortOrder.Ascending:
        if key is None:
            while hi != lo and l[mi] != v:
                if v > l[mi]:
                    lo = mi + 1
                else:
                    hi = mi
                mi = (hi + lo) // 2
            if l[mi] == v:
                return mi
        else:
            cv = key(l[mi])
            while hi != lo and cv != v:
                if v > cv:
                    lo = mi + 1
                else:
                    hi = mi
                mi = (hi + lo) // 2
                cv = key(l[mi])
            if cv == v:
                return mi
    else:
        if key is None:
            while hi != lo and l[mi] != v:
                if v < l[mi]:
                    lo = mi + 1
                else:
                    hi = mi
                mi = (hi + lo) // 2
            if l[mi] == v:
                return mi
        else:
            cv = key(l[mi])
            while hi != lo and cv != v:
                if v < cv:
                    lo = mi + 1
                else:
                    hi = mi
                mi = (hi + lo) // 2
                cv = key(l[mi])
            if cv == v:
                return mi

    if search_type == SearchType.Aprox:
        return mi
    else:
        if not_found_behavior == NotFoundBehavior.RaiseError:
            raise RuntimeError("Value not found")
        else:
            return None


class JsonList(list):
    def __init__(self, list_type=None, iterable=None, allow_empty: bool = False):
        iterable = list() if not iterable else iterable
        iter(iterable)
        map(self._typeCheck, iterable)
        list.__init__(self, iterable)
        self.list_type = list_type
        self.allow_empty = allow_empty

    @staticmethod
    def create_type(list_item_type: type, list_type_name: str = "") -> type:
        def __init__(self, iterable=None):
            JsonList.__init__(self, iterable=iterable, list_type=list_item_type)
        if not list_type_name:
            list_type_name = "Json_%s_list" % list_item_type.__name__
        newclass = type(list_type_name, (JsonList,), {"__init__": __init__})
        return newclass


    def _typeCheck(self, val):
        if val is None and self.allow_empty:
            return
        if self.list_type:
            if self.list_type is float and type(val) is int: #json ints can also be floats
                val = float(val)
            check_type(val, self.list_type, "Wrong type %s, this list can hold only instances of %s" % (type(val), str(self.list_type)))
        else:
            if not (issubclass(type(val), JsonObject) or isinstance(val, (str, int, float, bool, datetime, JsonList))):
                raise TypeError("Wrong type %s, this list can hold only str, int, float, bool, datetime, JsonObject or JsonList" % (type(val),))

    def __iadd__(self, other):
        map(self._typeCheck, other)
        list.__iadd__(self, other)
        return self

    def __add__(self, other):
        iterable = [item for item in self] + [item for item in other]
        return JsonList(list_type=self.list_type, iterable=iterable)

    def __radd__(self, other):
        iterable = [item for item in other] + [item for item in self]
        if isinstance(other, JsonList):
            return self.__class__(list_type=other.list_type, iterable=iterable)
        return JsonList(list_type=self.list_type, iterable=iterable)

    def __setitem__(self, key, value):
        itervalue = (value,)
        if isinstance(key, slice):
            iter(value)
            itervalue = value
        map(self._typeCheck, itervalue)
        list.__setitem__(self, key, value)

    def __setslice__(self, i, j, iterable):
        iter(iterable)
        map(self._typeCheck, iterable)
        list.__setslice__(self, i, j, iterable)

    def append(self, val):
        self._typeCheck(val)
        list.append(self, val)

    def extend(self, iterable):
        iter(iterable)
        map(self._typeCheck, iterable)
        list.extend(self, iterable)

    def insert(self, i, val):
        self._typeCheck(val)
        list.insert(self, i, val)

    def __str__(self):
        return "[" + ",".join([json.dumps(x) if type(x) is str else "null" if x is None else str(x) for x in self]) + "]"

    def __repr__(self):
        return str(self)

    def get(self, m):
        l = JsonList()
        for i in self:
            if m in vars(i):
                l.append(vars(i)[m])
        return l

    def where(self, m: str, v, o: str = "=="):
        d = {}
        if type(v) is str:
            criteria = "def criteria(i): return i.%s %s '%s'" % (m, o, v)
        elif isinstance(v, JsonObject):
            criteria = "def criteria(i): return str(i.%s) %s '%s'" % (m, o, str(v))
        else:
            criteria = "def criteria(i): return i.%s %s %s" % (m, o, str(v))

        exec(criteria, d)
        return self.filter(d["criteria"])

    def split_by(self, m) -> dict:
        if type(m) is str and issubclass(self.list_type, JsonObject):
            d = {}
            exec("def criteria(i): return i.%s" % m, d)
            m = d["criteria"]
        r = {}
        for i in self:
            l = m(i)
            if l not in r:
                r[l] = self.__class__()
                self.list_type = self.list_type
            r[l].append(i)
        return r

    def filter(self, key):
        nl = self.__class__()
        for i in self:
            if key(i):
                nl.append(i)
        return nl

    def find_first(self, key, not_found_behavior=NotFoundBehavior.RaiseError):
        i = self.find_first_index(key, not_found_behavior=not_found_behavior)
        return None if i is None else self[i]

    def find_first_index(self, key, not_found_behavior=NotFoundBehavior.RaiseError):
        if callable(key):
            for ix, i in enumerate(self):
                if key(i):
                    return ix
        else:
            for ix, i in enumerate(self):
                if key == i:
                    return ix

        if not_found_behavior == NotFoundBehavior.RaiseError:
            raise RuntimeError("Value not found")
        else:
            return None

    def find_ordered(self, value, key=None, search_type=SearchType.Exact, order=SortOrder.Ascending, not_found_behavior=NotFoundBehavior.RaiseError):
        i = bin_search(self, value, key=key, search_type=search_type, order=order, not_found_behavior=not_found_behavior)
        return None if i is None else self[i]

    def find_ordered_index(self, value, key=None, search_type=SearchType.Exact, order=SortOrder.Ascending, not_found_behavior=NotFoundBehavior.RaiseError):
        return bin_search(self, value, key=key, search_type=search_type, order=order, not_found_behavior=not_found_behavior)

    def process(self, l):
        nl = JsonList()
        for i in self:
            nl.append(l(i))
        return nl

    def copy(self):
        return self.__class__.parse(str(self))

    @classorinstancemethod
    def parse(cls_or_self, json_string="", json_list=None):
        if json_string:
            check_type(json_string, str, "wrong type for json_string")
            json_list = json.loads(json_string)
        check_type(json_list, list, "wrong type for json_list")
        if type(cls_or_self) is type:
            new_list = cls_or_self()
        else:
            new_list = cls_or_self
            new_list.clear()
        it = new_list.list_type
        ic = it().__class__
        for i in json_list:
            if i is None:
                new_list.append(i)
            elif issubclass(ic, JsonObject):
                new_list.append(it.parse(json_dictionary=i))
            elif issubclass(ic, JsonList):
                new_list.append(it.parse(json_list=i))
            elif issubclass(ic, datetime):
                new_list.append(datetime.strptime(i, JsonDate.date_format))
            elif issubclass(ic, JsonString):
                new_list.append(JsonString(i))
            else:
                new_list.append(i)
        return new_list

    def save(self, file_path: str):
        with open(file_path, 'w') as f:
            f.write(str(self))

    def load_from_file(self, file_path: str):
        if not path.exists(file_path):
            return None
        json_content = ""
        with open(file_path) as f:
            json_content = f.read()
        return self.parse(json_content)

    def load_from_url(self, uri: str):
        req = requests.get(uri)
        if req.status_code == 200:
            return self.parse(req.text)
        return None

    def to_numpy_array(self):
        from numpy import array
        if self.list_type is int or self.list_type is float or self.list_type is bool:
            return array(self)
        return array([i.get_values() for i in self if isinstance(i, JsonObject)])

    def from_numpy_array(self, a):
        self.clear()
        columns = self.list_type().get_columns()
        for row in a:
            ni = self.list_type()
            for i, c in enumerate(columns):
                ni[c] = row[i]
            self.append(ni)

    def to_dataframe(self, recursive: bool = False):
        from pandas import DataFrame
        if self.list_type is JsonObject or self.list_type is None:
            if len(self) == 0:
                return DataFrame()
            if isinstance(self[0], JsonObject):
                columns = self[0].get_columns()
            else:
                raise RuntimeError("Item type cannot be loaded to dataframe")
        else:
            if issubclass(self.list_type, JsonObject):
                columns = self.list_type().get_columns()
            else:
                return DataFrame(self)

        if recursive:
            return DataFrame([i.__dataframe_values__() for i in self], columns=columns)
        else:
            return DataFrame([i.get_values() for i in self], columns=columns)

    def from_dataframe(self, df):
        self.clear()
        columns = df.columns
        for i, row in df.iterrows():
            ni = self.list_type()
            for c in columns:
                ni[c] = row[c]
            self.append(ni)


class JsonString(str):
    def __new__(cls, string=""):
        if string:
            try:
                o = JsonObject.load(string)
                instance = super().__new__(cls, str(o))
                setattr(instance, "value", o)
            except:
                instance = super().__new__(cls, string)
                setattr(instance, "value", None)
        else:
            instance = super().__new__(cls)
        return instance
