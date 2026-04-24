# Python-Tickers-01

Application script is main.py, coded in Python 3.11.2



Execution Sequence:

• Fetch application root path using fetch\_root function from fetch\_root.py

• Application originally imported two years of data per ticker as base content.

&#x20; Application then determines start date ten days ago.

&#x20; This is done to optimize performance.

&#x20; Uses fetch\_start\_date function from fetch\_start\_date.py

• List of Tickers loaded into list using fetch\_tickers function from fetch\_tickers.py

&#x20; The fetch\_tickers function loads ticker list from tickers.ini file

• Loop through tickers, for each load last 10 days of ticker prices using yFinance Python module

&#x20; Delta prices loaded to master files in Data subfolder with .JO extensions in CSV format

• Start with Analytics:

&#x20; \* For each ticker, load .JO content into Pandas DataFrame

&#x20; \* (i) Determine average close price per year per ticker. Average is calculated only on data available.

&#x20;       Public holidays and weekend ignored. Average then based only on content available.

&#x20; \* (ii) Using a list comprehension filter, determine number of days per year per ticker with less 

&#x20;   than a million trades per day.

&#x20; \* Pivot both sets by year and write away to Data subfolder as .sum file

&#x20; \* For each ticker, read content from .sum files and concatenate as JSON summary

&#x20; \* write JSON summary away as .JSON file

&#x20; \* submit JSON content to webhook https://steep-bird-28.webhook.cool

&#x20; \* response 200 indicate valid JSON content.



Recommendations:

All content in Data folder is in CSV format with heavy disk footprint. Recommend using parquet.

In Parquet files, columns are data type aware, content is compressed and in binary.

&#x20; 

