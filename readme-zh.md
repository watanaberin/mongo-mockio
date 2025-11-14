# mongo-mockio

## 项目描述
`mongo-mockio`是模拟MongoDB数据工具，利用提供的 JSON 文件模板，通过命令行操作或web页面来模拟数据。它内置了诸如（choose/chooses/between）等函数，并已接入Faker数据库，用户只需使用`$faker.xxx`标志符进行调用。并且，它还支持用户自定义数据源来模拟bson对象。

## 技术堆栈
- MongoDB
- JSON
- Command Line
- Flask

## 设置和安装
1. 克隆本仓库或下载代码库
2. 使用 pip 安装必要的依赖 (`pip install -r requirement.txt`)
3. 修改模板文件以满足您的模拟数据需求
4. 通过命令行或启动 http 服务(`flask run -> open localhost:5000`) 配置数据库等相关配置将模拟数据插入到MongoDB中

### 配置优先级
* 命令行
1, command line, 
2, .env file
3, default 
* http 服务
1. web 参数

## 使用说明
在提供的 JSON 模板文件中，你可以使用内置函数，如`$choose`、`$chooses`、和`$between`，或者接入Faker数据库进行数据模拟，只需使用`$faker.xxx`标志符进行调用。

同时也支持使用你自己定义的数据源来模拟 BSON 对象, 在`source/ `文件下添加 {custom}.json 文件, 在 JSON 模版文件中就能够使用 `${custom}` 来作为数据源。

目前支持的内置函数:
|   Operators |      Output
|  ---------  | -----------------------------  
|    $ip      |     "x.x.x.x" | ["x.x.x.x"...]  
|    $country |     Any | [Any...]  
|    $region  |     Any | [Any...] 
|    $incrementIntId | begin from 1 ...  
|   $[custom] |     Any | [Any...]  
|   $faker.method() | Any


```json
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

example:
``` json
{ 
    'name': 'Jihyo',
    'age': 88,
    'sex': 'female',
    'area': { 'country': 
    ['Aruba', 'Kiribati', 'Brunei Darussalam', 'Gambia', 'Dominican Republic', 'Belarus', 'Philippines', 'Burundi'],
    'region': 'Africa' },
    'birthday': datetime.datetime(1991, 5, 4, 8, 5, 5),
    'peer': { 'first': 'know it',
    'second': 'known' },
    'lastLoginAt': '89.66.239.224' 
} 
```