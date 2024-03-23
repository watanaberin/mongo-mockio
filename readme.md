# mongo-mockio
[Chinese](./readme-zh.md)
**mongo-mockio** is a tool for mocking data into mongodb from well defined JSON file. It supports command line and web service to help mocking data into MongoDB.
Here is an example in mongo-mockio:

1. Create a JSON file as temp.json
In the first layer, 'user' is the MongoDB Collection name
In the second layer, the key of the JSON body is the field of the collection
```
{
    "user": {
        "name": {"$choose": "$name"},
        "address": "$facker.address()",
        "age": {"$between": [21, 99]},
        "sex": {"$choose": ["female", "male"]},
        "area": {        
            "country": {"$chooses": "$country"},
            "region": {"$choose": ["Europe", "Africa", "Americas", "Asia", "Oceania"]}
        },
        "birthday": { "$between": ["1990-03-26", "2000-12-29"]},
        "peer": {"$choose": [
            {
                "first": "dont know",
                "second": "Unknown"
            },
            {
                "first": "know it",
                "second": "known"
            }
        ]},
        "lastLoginAt": "$ip"
    }
}
```
2. cd mockio
3. python cmd.py -f temp.json -n 1201 -m 127.0.0.1:27017 -d prod

##### Operators

Operator is a function which requires dataset you wanna to set in the field
Usage: 
```
{
    "name" : {"$choose": ["kim", "kiki"]}
}
```

|   Operators |   Input Type      | PlaceHolder Support
|  ---------  | ----------------  | -------------------
|   $choose   |    [Any...]       |          Yes
|   $chooses  |    [Any...]       |          Yes
|   $between  | [str_date OR int] |           No


##### PlaceHolder

PlaceHolder is the source of data you add in mockio/source dictionary with some default source. It also support python Facker library, use '$facker.fackermethod()' to call.
eg. add source/city.json then you can use $city stands for a city list in source/city.json file.

|   Operators |      Output Type
|  ---------  | -----------------------------  
|    $ip      |     "x.x.x.x" | ["x.x.x.x"...]  
|    $country |     Any | [Any...]  
|    $region  |     Any | [Any...] 
|    $incrementIntId | begin from 1 ...  
|   $[custom] |     Any | [Any...]  
|   $faker.method() | Any

```
{
    "city" : {"$choose": "$city"}
}
```

**Why & How to add a {custom} placeholder**

If you have a city list in json format and want to use it as a data source, you can save the city list in the format of city.json file and place it under the resource folder, so you can use $city to get your data

1. add {custom}.json file to source dictionary
2. {custom}.json file requires list format
3. then you can use ${custom} as placeholder

#### How to use

- [Required] install
```
    pip install -r requirement.txt
```
- [Optional] make own placeholder
- [Required] write a template json file
```
{
    "user": {
        "name": {"$choose": "$name"},
        "age": {"$between": [21, 99]},
        "sex": {"$choose": ["female", "male"]},
        "area": {        
            "country": {"$chooses": "$country"},
            "region": {"$choose": ["Europe", "Africa", "Americas", "Asia", "Oceania"]}
        },
        "birthday": { "$between": ["1990-03-26", "2000-12-29"]},
        "peer": {"$choose": [
            {
                "first": "dont know",
                "second": "Unknown"
            },
            {
                "first": "know it",
                "second": "known"
            }
        ]},
        "lastLoginAt": "$ip"
    }
}
```
* cmd
(1.) Use command line
    - python cmd.py -h
eg. python main.py -f temp.json -n 1201 -m 127.0.0.1:27017 -d prod
(2.) use .env file
```
Priority: 
1, command line, 
2, .env file
3, default 
```
* web
    - flask run
    

example:
```
{'name': 'Jihyo', 'age': 88, 'sex': 'female', 'area': {'country': ['Aruba', 'Kiribati', 'Brunei Darussalam', 'Gambia', 'Dominican Republic', 'Belarus', 'Philippines', 'Burundi'], 'region': 'Africa'}, 'birthday': datetime.datetime(1991, 5, 4, 8, 5, 5), 'peer': {'first': 'know it', 'second': 'known'}, 'lastLoginAt': '89.66.239.224'}
{'name': 'Tzuyu', 'age': 90, 'sex': 'female', 'area': {'country': ['United States of America', 'Kiribati', 'Germany', 'Zambia', 'Brazil', 'Austria', 'Angola', 'Curaçao', 'Jersey'], 'region': 'Africa'}, 'birthday': datetime.datetime(1993, 11, 25, 16, 31, 9), 'peer': {'first': 'dont know', 'second': 'Unknown'}, 'lastLoginAt': '119.225.158.21'}
```




