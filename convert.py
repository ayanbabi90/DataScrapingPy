
from io import StringIO
from typing import Match
import pandas as pd
import operator
from objdict import ObjDict
import os
import glob
#import json
import uuid
from decimal import Decimal
import simplejson as json
from pandas.core.dtypes.missing import notnull

path = os.getcwd()

fruitsData = glob.glob(os.path.join("./downloadedCSV/fruits", "*.csv"))
vegitableData = glob.glob(os.path.join("./downloadedCSV/vegitables", "*.csv"))

dairyData = glob.glob(os.path.join("./downloadedCSV/Dairy", "*.csv"))
grainsData = glob.glob(os.path.join("./downloadedCSV/Grains", "*.csv"))
proteinNonVegData = glob.glob(os.path.join(
    "./downloadedCSV/Protein_Non_veg", "*.csv"))
proteinVegData = glob.glob(os.path.join(
    "./downloadedCSV/Protein_Veg", "*.csv"))


allJSON = []

ultimateJSON = []


def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)


def fetchFoodDetails(catogery, data):

    for f in data:
        _uuid = str(uuid.uuid4())
        jdata = {}
        jdata['sku_uuid'] = _uuid
        jdata['category'] = catogery
        # print(f)
        data = pd.read_csv(f, sep='\t')
        for idx, i in enumerate(data.values):
            # print(i)
            if not operator.eq("# Downloaded from https://www.nutritionvalue.org ", i[0]):
                if idx == 0:
                    jdata["name"] = i[0].replace("# ", "")
                    #print("name: " +jdata["name"])
                if idx == 1:
                    jdata["basedOn"] = i[0].replace("# ", "")
                if idx > 2:
                    arrayList = i[0].split(", ")
                    key = i[0].split(", ")[0].replace(" ", "_").replace(
                        "n-3_acid_(", "").replace(")", "").replace("+", "")
                    # print(i[0]);
                    jsonData = {}

                    # if len(arrayList) == 3:
                    #  jsonData = {  "amount": arrayList[1].strip(), "unit": arrayList[2].strip(),} # "dv": arrayList[4].strip() }
                    if len(arrayList) == 4:
                        amount = Decimal(arrayList[1].strip())
                        #print('4 amount: ---- ' + str(amount))
                        # "dv": arrayList[4].strip() }
                        jsonData = {"amount": amount,
                                    "unit": arrayList[2].strip(), }
                    elif len(arrayList) == 5:
                        amount = Decimal(arrayList[2].strip())
                        #print('5 amount: ---- ' + str(amount))
                        # "dv": arrayList[4].strip() }
                        jsonData = {"amount": amount,
                                    "unit": arrayList[3].strip(), }

                    # if len(arrayList) >= 4:
                    #    jsonData = {  "amount": arrayList[2].strip(), "unit": arrayList[3].strip(),} # "dv": arrayList[4].strip() }
                    # else:
                    #    jsonData = {  "amount": arrayList[1].strip(), "unit": arrayList[2].strip(),} # "dv": arrayList[3].strip() }
                    jdata[key] = jsonData
                    print('key: ' + key + ' len: ' + str(len(arrayList)))

        if jdata.__len__() > 0:
            allJSON.append(jdata)


fetchFoodDetails('fruit', fruitsData)
fetchFoodDetails('vegitable', vegitableData)
fetchFoodDetails('dairy', dairyData)
fetchFoodDetails('grains', grainsData)
fetchFoodDetails('proteinNonVeg', proteinNonVegData)
fetchFoodDetails('proteinVeg', proteinVegData)

print(allJSON)

for item in allJSON:
    if item not in ultimateJSON:
        ultimateJSON.append(item)

if ultimateJSON.__len__() > 0:
    writeToJSONFile('convertedJSON', 'convertedJSON', ultimateJSON)

print('Script END')
