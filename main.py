#To run Selenium in Replit IDE
#https://replit.com/talk/ask/Can-I-use-selenium/11566

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
import pandas as pd

options = Options()
options.add_argument("--window-size=1920x1080")
options.headless = True #Headless = No GUI

#add these two lines if running from replit IDE!!!!
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
driver.get("https://saultonline.com/lowest-gas-prices/")

items = driver.find_element(By.TAG_NAME, "table")
gasdata = items.text
#gasdata = items.text.replace("\n","/")
#print(gasdata)
#print()

headings = {'Station','Time'}
cities = {'Echo Bay','Sault Ste Marie','Bruce Mines','Thessalon','Desbarats'}
stations = {'Heyden Fuels','Esso',"Mac's",'Circle K',"Canadian Tire","Shell",'Petro-Canada','Flying J','Pit Stop'}

for heading in headings:
  gasdata = gasdata.replace(f"{heading}",f"/{heading}")
for station in stations:
  gasdata = gasdata.replace(f"{station}\n",f"/{station}, ")
for city in cities:
  gasdata = gasdata.replace(f"\n{city}\n",f", {city}/")
print(gasdata)
print()
#print(type(items.text)) #<class 'str'>

#Copies Gas Station Data to CSV (can be used for diagnosis)
text_file = open("ssmgas.csv", "w")
n = text_file.write(gasdata)
text_file.close()

driver.quit() #terminates the browser

df = pd.read_csv("ssmgas.csv", sep="/")
df.drop(df.tail(1).index,inplace=True) # drop last row
print(df)
print()

mingas = df[df['Price ']==df['Price '].min()] #station(s) with cheapest gas is stored here
mingas.reset_index(inplace = True, drop = True)
n = len(mingas) #no of rows/no of stations
print('Lowest gas price in SSM')
for i in range(0,n):  
 print(mingas['Price '][i], mingas['Station '][i])
 print(mingas['Time'][i]) 
print()
#this creates a file if it doesnt exist & skips headers if they already exist
with open("ssmmingas.csv",mode='a') as f:
  mingas.to_csv(f,header=f.tell()==0,sep='/',index=False)

#CSV file is read into dataframe & duplicate rows are removed
dup = pd.read_csv('ssmmingas.csv',sep='/')
no_dup = dup.drop_duplicates(keep='first')
no_dup.to_csv('ssmmingas.csv',sep='/', index = False)

maxgas = df[df['Price ']==df['Price '].max()] #station(s) with costliest gas is stored here
maxgas.reset_index(inplace = True, drop = True)
n = len(maxgas) #no of rows/no of stations
print('Highest gas price in SSM')
for i in range(0,n):  
 print(maxgas['Price '][i], maxgas['Station '][i])
 print(maxgas['Time'][i]) 
print()
#this creates a file if it doesnt exist & skips headers if they already exist
with open("ssmmaxgas.csv",mode='a') as f:
  maxgas.to_csv(f,header=f.tell()==0,sep='/',index=False)

#CSV file is read into dataframe & duplicate rows are removed
dup = pd.read_csv('ssmmaxgas.csv',sep='/')
no_dup = dup.drop_duplicates(keep='first')
no_dup.to_csv('ssmmaxgas.csv',sep='/', index = False)