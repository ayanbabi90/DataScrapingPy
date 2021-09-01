
from io import StringIO
import pandas as pd
import operator
from objdict import ObjDict
import os
import glob
import json

from pandas.core.dtypes.missing import notnull

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

path = os.getcwd()
csv_files = glob.glob(os.path.join("./downloadedCSV", "*.csv"))

allJSON = []

for f in csv_files:
    jdata = {}
    print(f)
    data = pd.read_csv(f, sep='\t') 
    for idx, i in enumerate(data.values):
        if not operator.eq("# Downloaded from https://www.nutritionvalue.org ", i[0]):
            if idx == 0:
                jdata["name"] = i[0].replace("# ", "")
            if idx == 1:
                jdata["basedOn"] = i[0].replace("# ", "")
            if idx > 2:
                arrayList = i[0].split(", ")
                key = i[0].split(", ")[0].replace(" ", "_")
                jdata[key] = { "amount": arrayList[1].strip(), "unit": arrayList[2].strip(), "dv": arrayList[3].strip() }
    
    if jdata.__len__() > 0:
        allJSON.append(jdata)

if allJSON.__len__() > 0:
   writeToJSONFile('convertedJSON','convertedJSON',allJSON)
    
print('Script END')
