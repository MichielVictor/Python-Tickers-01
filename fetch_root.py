import os

def fetch_root():
   script_path = os.path.abspath(__file__)
   script_path = script_path.replace("fetch_root.py","")
   return script_path



