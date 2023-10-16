import json
import collections.abc
import random
import string


class DB:

    def __init__(self, dbname):
        self.filename = str(dbname) + ".json"
        pass

    def value(self) -> dict:
        file = open(self.filename, "r")
        result = json.loads(file.read())
        file.close()
        return result

    def set(self, data):
        file = open(self.filename, "w")
        file.write(json.dumps(data, indent=2))
        file.close()
        self.data = json.dumps(data, indent=2) 
        pass

    def __getupdate(self, dic, new) -> dict:
        for key, value in new.items():
            if isinstance(value, collections.abc.Mapping):
                y = dic.get(key, {})
                dic[key] = self.__getupdate(y, value)
            else:
                dic[key] = value
        return dic

    def update(self, new):
        updated = self.__getupdate(self.value(), new)
        self.set(updated)
        pass
            
    def format(self):
        self.set(self.value())
        pass

    def delete(self, key):
        db = self.value()
        del db[key]
        self.set(db)


def getrandkey(length) -> str:
    return ''.join(random.choices(string.ascii_letters, k=length))


def newDB(dbname):
    db = open(dbname+".json", "w")
    db.write("{}")
    db.close()
    return DB(dbname)
