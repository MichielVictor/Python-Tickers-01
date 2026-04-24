
import yfinance as yf
import os

#Get application root path
from fetch_root import fetch_root
sRoot = fetch_root()
'''print("Root:",sRoot)'''

#Get start date -> first of Jan two years ago
from fetch_start_date import fetch_start_date
dtStart,sDtStart = fetch_start_date()
'''print("dtStart:",dtStart,"sDtStart:",sDtStart)'''

#Retrieve Ticker's codes and descriptions into seperate lists
from fetch_tickers import fetch_tickers
Tickers = []
Ticker_desc = []
Tickers, Ticker_desc = fetch_tickers()

#Loop through Tickers
'''Tickers = ["NPN.JO"]'''
for sTicker in Tickers:
   sTickerParts = sTicker.split(".")
   sTickerFile = sTickerParts[0].strip() + ".csv"
   fCSV = sRoot + "Data\\" + sTickerFile
   fJO = sRoot + "Data\\" + sTicker
   fSUM = sRoot + "Data\\" + sTicker + '.sum'
   print(sTicker)
   '''
   print(fCSV)
   print(fJO)
   '''

   #Download prices for ticker for period in csv
   data = yf.download(sTicker, start=sDtStart, auto_adjust=True)
   data.to_csv(fCSV)

   #Read JO Master file
   with open(fJO.strip(), "r", encoding="utf-8") as f:
      JOcontent = f.read()
      f.close()

   #Read downloaded CSV file
   with open(fCSV.strip(), "r", encoding="utf-8") as f:
      CSVcontent = f.read()
      f.close()

   #Write delta to master file
   CSV = CSVcontent.split("\n")
   for lines in CSV:
      if len(lines.strip()) > 0 and not lines[:10] in JOcontent and lines[0] in ["0","1","2","3","4","5","6","7","8","9"]:
         JOcontent = JOcontent + lines + '\n'
      with open(fJO.strip(), "w", encoding="utf-8") as f:
         f.write(JOcontent)
         f.close()
   #Delete downloaded CSV file
   os.remove(fCSV.strip())

   #Start with analytics
   import pandas as pd

   df = pd.read_csv(fJO, header=None)

   df.rename(columns={df.columns[0]: "Date"}, inplace=True)
   df.rename(columns={df.columns[1]: "Close"}, inplace=True)
   df.rename(columns={df.columns[2]: "High"}, inplace=True)
   df.rename(columns={df.columns[3]: "Low"}, inplace=True)
   df.rename(columns={df.columns[4]: "Open"}, inplace=True)
   df.rename(columns={df.columns[5]: "Volume"}, inplace=True)

   #Force Date column as datetime
   df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
   df["Year"] = df["Date"].dt.year
   #Force columns to appropriate data types
   df["Close"] = df["Close"].astype(float)
   df["High"] = df["High"].astype(float)
   df["Low"] = df["Low"].astype(float)
   df["Open"] = df["Open"].astype(float)
   df["Volume"] = df["Volume"].astype(int)

   #Average Close price by year
   avg_close_by_year = df.groupby(df["Date"].dt.year)["Close"].mean()
   '''print(avg_close_by_year)'''

   #Pivot results by year
   result_df = avg_close_by_year.to_frame().T
   '''print(result_df)'''

   #List comprehension to filter number of days per year where volume less than a million
   counts_by_year = {
       year: sum((df["Year"] == year) & (df["Volume"] < 1000000))
       for year in df["Year"].unique()
   }
   '''print(counts_by_year)'''

   pivoted = pd.DataFrame([counts_by_year])
   '''print(pivoted)'''

   num_years = pivoted.shape[1]
   '''print(num_years)'''

   sHeaders = "Ticker,Measure,"
   for i in range(0, num_years):
      sHeaders = sHeaders + str(result_df.columns[i]) + ","
   sHeaders = sHeaders[:-1] + "\n"
   sHeaders = sHeaders + sTicker+ ",AVG_Close_Price,"
   for i in range(0, num_years):
      sHeaders = sHeaders + str(result_df.iloc[0, i]) + ","
   sHeaders = sHeaders[:-1] + "\n"
   sHeaders = sHeaders + sTicker + ",<1M,"
   for i in range(0, num_years):
      sHeaders = sHeaders + str(pivoted.iloc[0, i]) + ","
   sHeaders = sHeaders[:-1]

   with open(fSUM.strip(), "w", encoding="utf-8") as f:
      f.write(sHeaders)
      f.close()

#Start with JSON summary
sJSON = "[" + "\n"

for sTicker in Tickers:
   sTickerParts = sTicker.split(".")
   sTickerFile = sTickerParts[0].strip() + ".csv"
   fSUM = sRoot + "Data\\" + sTicker + '.sum'
   fJSON = sRoot + "Data\\Tickers.JSON"

   df = pd.read_csv(fSUM, header=0)

   for i in range(df.shape[0]):
       sJSON = sJSON + "{" + "\n"
       for j in range(df.shape[1]):
           sJSON = sJSON + "\"" + str(df.columns[j]) + "\"" + ":" + "\"" + str(df.iloc[i, j]) + "\"" + "," + "\n"
       sJSON = sJSON[:-2] + "\n"    
       sJSON = sJSON + "}," + "\n"
    
sJSON = sJSON[:-2] + "\n"
sJSON = sJSON + "]"

with open(fJSON.strip(), "w", encoding="utf-8") as f:
   f.write(sJSON)
   f.close()

#Webhook
import requests

url = "https://steep-bird-28.webhook.cool"

data = sJSON

response = requests.post(url, json=data)

print("Webhook Response:",response.status_code)

print("Done")
   
