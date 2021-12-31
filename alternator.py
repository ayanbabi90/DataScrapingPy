
import os
import json


f = open('./multipurposeJSON/foods.json')

data = json.load(f)

# for key in data:
#     print(key);
#     print(data[key]);

strKeys = {""}
strExcludedKeys = ["_id", "sku_uuid", "category", "name", "basedOn"]
allJSON = []

for item in data:
    # print(item)
    for key,val in item.items():
        #print(key)
        if not (key) in strExcludedKeys:
            strKeys.add(str(item))

    # if not (item) in strExcludedKeys:
    #     print(json.dumps(item, indent=1))
        
        #strKeys.add(str(item))

# for key in strKeys:
#     print(json.dumps(key, indent=1))

unitMap = {}

for item in data:
    obj = {}
    for key in item:
        if not (key) in strExcludedKeys:
            obj[key] = item[key]['amount']
            unitMap[key] = item[key]['unit']
        elif not key == '_id':
            obj[key] = item[key]
    allJSON.append(obj)


def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)



if allJSON.__len__() > 0:
    writeToJSONFile('convertedJSON', 'convertedToNewJSON', allJSON)
if unitMap.__len__() > 0:
    writeToJSONFile('convertedJSON', 'unitJSON', unitMap)

f.close()
