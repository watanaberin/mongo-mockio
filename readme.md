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



**Why & How to add a {custom} placeholder**
If you have a city list in json format and want to use it as a data source, you can save the city list in the format of city.json file and place it under the resource folder, so you can use $city to get your data

1. add {custom}.json file to source dictionary
2. {custom}.json file requires list format
3. then you can use ${custom} as placeholder

#### How to use

- <Required> install
- <Required> write a template json file
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
- <Optional> python main.py -h
- <Optional> make own placeholder
- <Required> exec

data be like:
```
{'name': 'Jihyo', 'age': 88, 'sex': 'female', 'area': {'country': ['Aruba', 'Kiribati', 'Brunei Darussalam', 'Gambia', 'Dominican Republic', 'Belarus', 'Philippines', 'Burundi'], 'region': 'Africa'}, 'birthday': datetime.datetime(1991, 5, 4, 8, 5, 5), 'peer': {'first': 'know it', 'second': 'known'}, 'lastLoginAt': '89.66.239.224'}
{'name': 'Tzuyu', 'age': 90, 'sex': 'female', 'area': {'country': ['United States of America', 'Kiribati', 'Germany', 'Zambia', 'Brazil', 'Austria', 'Angola', 'Curaçao', 'Jersey'], 'region': 'Africa'}, 'birthday': datetime.datetime(1993, 11, 25, 16, 31, 9), 'peer': {'first': 'dont know', 'second': 'Unknown'}, 'lastLoginAt': '119.225.158.21'}
```




