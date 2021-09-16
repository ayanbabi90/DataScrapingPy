
import pandas as pd
import os
import json
import requests
import webbrowser
from bs4 import BeautifulSoup
import operator

print('/n/n==========Script Started========/n/n')

nameList = []
idList = []
urlList = []
foodList = ['fruits','vegetables','Grains','Protein_Veg','Protein_Non_veg','Dairy']

with open('./FoodList.json') as f:
  data = json.load(f)
  for i in data[foodList[5]]:
      url = "https://www.nutritionvalue.org/foodsuggest.php?token="+i
      response = requests.get(url=url,headers={'User-Agent': 'Mozilla'})
      body = response.json()[0][1]["t"]
      nextUri = 'https://www.nutritionvalue.org/'+body[0]+'%2C_raw_'+body[1]+'_nutritional_value.html?size=100+g'
      if not operator.eq(body[0],body[1]):
        nextRequest = requests.get(url=nextUri,headers={'User-Agent': 'Mozilla'})
        soup = BeautifulSoup(nextRequest.text,features="html.parser")
        for line in soup.find_all('a'):
            uri = line.get('href')
            if operator.contains(uri, "data:text/csv"):
                    webbrowser.open(uri, new=2)
                    nameList.append(body[0])
                    idList.append(body[1])
                    urlList.append(nextUri)            

df = pd.DataFrame({'Id':idList, 'Name':nameList, 'Uri': urlList})
df.to_excel('./foodNameAndId.xlsx', sheet_name='Fruites')

print('/n/n========= Extercetion End =========')
