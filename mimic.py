import json
import string
import random

# public a string of random characters
def randomID():
    return "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(8)]
    )


# param directory to json file, returns json file in the form of an object
def getJSONObject(fileName):
    with open(fileName, "r") as file:
        return json.load(file)


# param object, returns converts an object into a json string
def getJSONString(dataBase):
    return json.dumps(dataBase, indent=3)


# param directory to json file, object to write to the json file
def writeJSON(fileName="./mimic.json", data=None):
    if data is not None:
        with open(fileName, "w") as file:
            return file.write(getJSONString(data))


class Collection:
    def __init__(self, key):
        self._id = key
        self.fn = "./mimic.json"
        self.body = getJSONObject(self.fn)[self._id]

    def refreshStore(self):
        db = getJSONObject(self.fn)
        db.update({self._id: self.body})
        writeJSON(self.fn, db)

    def toDict(self):
        return self.body

    def update_doc(self, _id, data):
        if _id in self.body:
            self.body[_id].update(data)
            db = getJSONObject(self.fn)
            db.update({self._id: self.body})
            writeJSON(self.fn, db)
        else:
            print("_id: ", _id, " doesnt exists")

    def deleteKey(self, key=None):
        if key in self.body:
            del self.body[key]
            self.refreshStore()
        else:
            print("Error:", key, " does not exist")

    def clear_doc(self, key=None):
        if key in self.body:
            self.body[key] = {}
            self.refreshStore()

    def delete_doc(self, key=None, doc=None):
        if key in self.body:
            del self.body[key][doc]
            self.refreshStore()

    def insert(self, key=None, data=None):
        if key is None:
            key = randomID()
        if type(data) != type({}):
            data = {"message": data}
        if key not in data:
            self.body[key] = data
            self.refreshStore()
        else:
            print(key, " already exists")

    def insertMany(self, _list=[]):
        key = None
        if len(_list) > 0:
            for d in _list:
                key = list(d.keys())
                if len(key) == 1:
                    self.insert(key[0], d[key[0]])
                else:
                    self.insert(randomID(), d)

    def getKeys(self):
        return list(self.body.keys())

    def find_all_docs(self, _target=None, _list_found=[], _count=0):
        listFound = _list_found
        _keys = self.getKeys()
        if _target in self.body[_keys][_count]:
            listFound.append(self.body[_keys[_count]])
            return self.find_all_docs(
                _target=_target, _list_found=listFound, _count=_count + 1
            )

    def find_doc(self, _id, key):
        try:
            return self.body[_id][key]
        except:
            print("error, key not found")

    def find(self, key):
        try:
            return self.body[key]
        except:
            print("error, key not found")


class Mime:
    # initializes database that refers to the json file
    def __init__(self, fn="./mimic.json"):
        self.fn = fn
        self.ref = getJSONObject(self.fn)

    # returns an object of the json file
    def toDict(self):
        return getJSONObject(self.fn)

    # param key and value, updates the database and rewrites the object to the database
    def update(self, key=None, values=None):
        db = getJSONObject(self.fn)
        if key in db:
            db.update({key: values})
            writeJSON(self.fn, db)
        else:
            print("Error:", key, " does not exist")

    # param new key and the old key to change
    def changeKey(self, newKey=None, oldKey=None):
        db = getJSONObject(self.fn)
        if newKey in db:
            print("Error:", newKey, " already exists")
            return
        if oldKey not in db:
            print("Error:", oldKey, " does not exist in your database")
            return

        if newKey is not None and oldKey is not None:
            self.createCollection(newKey, self.collection(oldKey))
            self.destroyCollection(oldKey)

    # param key, targets a sub collection with a key of key
    def collection(self, key):
        return Collection(key)

    # returns an array of all keys in the database
    def getCollectionKeys(self):
        get_dict = getJSONObject(self.fn)
        return list(get_dict.keys())

    # param key and data, adds a new key to the database with data
    def createCollection(self, key=None, data={}):
        db = getJSONObject(self.fn)
        if key not in db:
            db[key.lower()] = data
            writeJSON(self.fn, db)
        else:
            print("Error:", key, " already exists")

    # param key, deletes a collection with a key of key
    def destroyCollection(self, key=None):
        db = getJSONObject(self.fn)
        if key in db:
            del db[key]
            writeJSON(self.fn, db)
        else:
            print("Error:", key, " does not exist")

    # clears the database
    def clear(self):
        with open(self.fn, "w") as file:
            file.write(getJSONString({}))
