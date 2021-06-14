# 參考資料
# 串API: https://jbprogramnotes.com/2021/04/%E4%BD%BF%E7%94%A8-python-%E5%B0%87%E8%B3%87%E6%96%99%E5%AF%AB%E5%85%A5-google-%E8%A9%A6%E7%AE%97%E8%A1%A8/
# 匯入dataframe進google worksheets: https://github.com/robin900/gspread-dataframe

import pandas as pd
from pandas import json_normalize
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
import time
from datetime import timedelta, datetime
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import requests, bs4
import json

# Sheet1

# Scraping data
url = "https://covid19dashboard.cdc.gov.tw/dash3"
html = requests.get(url)
objSoup = bs4.BeautifulSoup(html.text, 'lxml')

# str to dataframe
dict_item1 = json.loads(objSoup.p.text)
df = json_normalize(dict_item1['0']) #Results contain the required data

# Add column of mortality rate
df['死亡率'] =df.at[0,'死亡']/int(df.at[0,'確診'].replace(",",""))

# Save data
timestr = time.strftime("%Y%m%d")
df.to_csv('DATASHEETS_COVD19_1/COVID19_1_'+timestr+'.csv', encoding="utf_8_sig")
df.to_csv('DATASHEETS_COVD19_1/COVID19_1.csv', encoding="utf_8_sig")

# google sheets authentication
Json = './covid19.json'
Url = ['https://spreadsheets.google.com/feeds']
# 連線到資料表
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)
# 開啟資料表及工作表
Sheet = GoogleSheets.open_by_key('1ukNfvu7G5OQdKNZpXmyN0XHctwvsByjEbvh5WlUMynY')
# Sheets = Sheet.sheet1
# 查看此 GoogleSheet 內 Sheet 清單
wks_list = Sheet.worksheets()
#選取by名稱
worksheet = Sheet.sheet1
#寫入資料
set_with_dataframe(worksheet, df)
print("Sheet1寫入成功")

# Sheet2

# Scrape data & Clean data
url = "https://nidss.cdc.gov.tw/nndss/DiseaseMap?id=19CoV"
html = requests.get(url)
objSoup = bs4.BeautifulSoup(html.text, 'lxml')
if objSoup !=None:
    item1 = objSoup.find(class_="map-chart").script
    item1 = str(item1)
items1 = "{" +item1[item1.index('.geojson",')+10:item1.index('],"properties"')]+"]}"
dict_item1 = json.loads(items1)
df = json_normalize(dict_item1['series']) #Results contain the required data
df.columns=['地區', '累積確診人數']

#儲存資料
timestr = time.strftime("%Y%m%d")
df.to_csv('DATASHEETS_COVD19_2/COVID19_2_'+timestr+'.csv', encoding="utf_8_sig")
df.to_csv('DATASHEETS_COVD19_2/COVID19_2.csv', encoding="utf_8_sig")
#取得昨日資料
yesterday = datetime.today() + timedelta(-1)
timestr_yesterday = yesterday.strftime('%Y%m%d')
df2 = pd.read_csv('DATASHEETS_COVD19_2/COVID19_2_'+timestr_yesterday+'.csv', index_col=0, thousands=',')
# assign merged key
df3 = pd.merge(df, df2, on='地區')
df3['新增確診人數'] = df3['累積確診人數_x'] - df3['累積確診人數_y']
#儲存資料
timestr = time.strftime("%Y%m%d")
df3.to_csv('DATASHEETS_COVD19_2/COVID19_2_new'+timestr+'.csv', encoding="utf_8_sig")
df3.to_csv('DATASHEETS_COVD19_2/COVID19_2_new.csv', encoding="utf_8_sig")

# 連線到資料表
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)
# 開啟資料表及工作表
Sheet = GoogleSheets.open_by_key('12ba57CqIauuqcYV93hUxwjmU7Wk_CoSLFytEuiuS1IQ')
# Sheets = Sheet.sheet1
# 查看此 GoogleSheet 內 Sheet 清單
wks_list = Sheet.worksheets()
#選取by名稱
worksheet = Sheet.sheet1
#寫入資料
set_with_dataframe(worksheet, df3)
print("Sheet2寫入成功")

# Sheet5

url = 'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/global_data/vaccine_data_global.csv'
df = pd.read_csv(url)
#儲存資料
timestr = time.strftime("%Y%m%d")
df.to_csv('DATASHEETS_COVD19_5/COVID19_5_'+timestr+'.csv', encoding="utf_8_sig")
df.to_csv('DATASHEETS_COVD19_5/COVID19_5.csv', encoding="utf_8_sig")

# only get Taiwan data
df = df[df['Country_Region']=='Taiwan*']

# google sheets authentication
Json = './covid19.json'
Url = ['https://spreadsheets.google.com/feeds']
# 連線到資料表
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)
# 開啟資料表及工作表
Sheet = GoogleSheets.open_by_key('1BbbIITkHWizP25sj2AKMABiER4MP8H7AUKK2o3swpfQ')
# Sheets = Sheet.sheet1
# 查看此 GoogleSheet 內 Sheet 清單
wks_list = Sheet.worksheets()
#選取by名稱
worksheet = Sheet.sheet1
#寫入資料
set_with_dataframe(worksheet, df)
print("Sheet5寫入成功")



# Sheet6

# url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/05-14-2021.csv"
# df = pd.read_csv(url)
# df = df[df['Country_Region']=='Taiwan*']
# print(df)

# Save History data
# for i in range(15,32):
#     url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/05-"+str(i)+"-2021.csv"
#     df2 = pd.read_csv(url)
#     df2 = df2[df2['Country_Region']=='Taiwan*']
#     df = pd.concat([df, df2], ignore_index=True)
# print(df)

# for i in range(1,10):
#     url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/06-0"+str(i)+"-2021.csv"
#     df2 = pd.read_csv(url)
#     df2 = df2[df2['Country_Region']=='Taiwan*']
#     df = pd.concat([df, df2], ignore_index=True)
# print(df)

# for i in range(10,12):
#     url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/06-"+str(i)+"-2021.csv"
#     df2 = pd.read_csv(url)
#     df2 = df2[df2['Country_Region']=='Taiwan*']
#     df = pd.concat([df, df2], ignore_index=True)
# print(df.head())

df = pd.read_csv('DATASHEETS_COVD19_6/COVID19_6.csv', encoding="utf_8_sig")

yesterday = datetime.today() + timedelta(-1)
timestr_yesterday = yesterday.strftime("%m-%d-%Y")
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"+timestr_yesterday+".csv"
df2 = pd.read_csv(url)
df2 = df2[df2['Country_Region']=='Taiwan*']
df2['Confirmed_shift'] = 0
df2['Newly Confirmed'] = 0
#add資料sheet1-6全部更新時間
time_update = time.strftime("%Y-%m-%d %H-%M-%S")
df2['All_Update'] = time_update
df = pd.concat([df, df2], ignore_index=True)

#add column
df['Confirmed_shift'] = df["Confirmed"].shift(1)
df['Newly Confirmed'] = df['Confirmed'] - df['Confirmed_shift']

df['Deaths_Shift'] = df["Deaths"].shift(1)
df['Newly Deaths'] = df['Deaths'] - df['Deaths_Shift']


#儲存資料
timestr = time.strftime("%Y%m%d")
df.to_csv('DATASHEETS_COVD19_6/COVID19_6_'+timestr+'.csv', encoding="utf_8_sig")
df.to_csv('DATASHEETS_COVD19_6/COVID19_6.csv', encoding="utf_8_sig")

# google sheets authentication
Json = './covid19.json'
Url = ['https://spreadsheets.google.com/feeds']
# 連線到資料表
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)
# 開啟資料表及工作表
Sheet = GoogleSheets.open_by_key('1Tw0_YTw9rq4WKzO1uD8mrGIGdLQAdSekmkpiWDft4TE')
# Sheets = Sheet.sheet1
# 查看此 GoogleSheet 內 Sheet 清單
wks_list = Sheet.worksheets()
#選取by名稱
worksheet = Sheet.sheet1
#寫入資料
set_with_dataframe(worksheet, df)
print("Sheet6寫入成功")
