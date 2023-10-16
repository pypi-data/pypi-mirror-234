# mypyjsondb

### A simple and lightweight JSON mock database for small projects

create a new database:

```
db = mypyjsondb.newDB("dbname")
```
---
access an existing database:
```
db = mypyjsondb.DB("dbname")
```
---
get the value of the database:
```
print(db.value()) #value in the form of a dict
```
---
set the value of the database:
```
db.set("hello": "world") #this rewrites the whole database file
```
---
update stuff to the datbase file:
```
db.update({"newkey": "newvalue"})
```
---
delete item from the database file:
```
x.delete("unwantedkey")
```
---
format the data in a database:
```
db.format()
```
