import json

with open('region-all.json', 'r') as f:
    source = json.load(f)

regions = set()
contries = set()

for s in source:
   regions.add(s['region'])
   contries.add(s['name'])

with open('region.json','w', encoding='utf-8') as f:
    f.write(json.dumps(list(regions)))
    
with open('country.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(list(contries)))