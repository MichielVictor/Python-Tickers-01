import os

def fetch_tickers():
   script_path = os.path.abspath(__file__)
   script_path = script_path.replace("fetch_tickers.py","")
   script_path = script_path+"tickers.ini"
   with open(script_path, "r", encoding="utf-8") as f:
      content = f.read()
   lines = content.splitlines()
   tickers = []
   ticker_desc = []
   for line in lines:
      cols = line.split(",")
      tickers.append(cols[0])
      ticker_desc.append(cols[1])
   return tickers, ticker_desc
