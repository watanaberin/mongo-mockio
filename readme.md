### mongo-mockio

**mongo-mockio** is a tool for mocking data into mongodb from template file

#### Description & Support features
##### Operators

|   Operators |   Input Type
|  ---------  | ------------  
|   $choose   |    [Any...]   
|   $chooses  |    [Any...]   
|   $between  | [str_date | int] 

##### PlaceHolder
|   Operators |      Output Type
|  ---------  | -----------------------------  
|    $ip      |     "x.x.x.x" | ["x.x.x.x"...]  
|    $country |     Any | [Any...]  
|    $region  |     Any | [Any...]   
|   $[custom] |     Any | [Any...]   
**How to add a {custom} placeholder**
1. add {custom}.json file to source dictionary
2. {custom}.json file requires list format

#### How to use

1. install
2. write a template json file
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
2. python main.py -h




