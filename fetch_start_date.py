from datetime import date, timedelta

def fetch_start_date():
   dtStart = date.today()
   dtStart = dtStart - timedelta(days=10)
   sDtStart = dtStart.strftime("%Y-%m-%d")
   return dtStart, sDtStart
