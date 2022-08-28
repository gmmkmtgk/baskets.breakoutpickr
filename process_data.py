import requests, zipfile, io
import pandas as pd
import os
from datetime import timedelta, datetime
import uuid
import glob
import shutil


def download_url_and_save_csv(url, save_path):
  request = requests.get(url)
  zip_file = zipfile.ZipFile(io.BytesIO(request.content))
  zip_file.extractall(save_path)

def get_weekdates(start_date, end_date):
  dates = []
  delta = timedelta(days=1)
  iter_date = start_date
  weekend_values = set([5, 6])
  while iter_date <= end_date:
      if iter_date.weekday() not in weekend_values:
        dates.append({"month": iter_date.strftime("%b").upper(), "date": iter_date.strftime("%d%b%Y").upper(), "year": iter_date.strftime("%Y")})
      iter_date += delta
  return dates

def download_bhavcopy_multiple_dates(start_date, end_date):
  dates = get_weekdates(start_date, end_date)
  for date in dates:
    try:
      download_url_and_save_csv("https://www1.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{date}bhav.csv.zip".format(year = date['year'], month = date['month'], date = date['date']),
    'C:/Users/Keshav/Desktop/baskets.breakoutpickr/stock-data')
    except:
      print("An exception occurred for the downloading csv for date:", date['date'])

def convert_dates(date_input): 
  date_obj = datetime.strptime(date_input, '%d-%b-%Y')
  return date_obj.strftime('%Y-%m-%d')

#here we are reading all csv and suppling it to main fuction 
def process_data_in_downloaded_csv():
  # dir_name = "/Users/smmaheshwari/Desktop/LinkedIn Learning/test/csv/"
  dir_name = "C:/Users/Keshav/Desktop/baskets.breakoutpickr/stock-data"
  df_list = []
  csv_files = glob.glob(os.path.join(dir_name, '*.csv'))
  for file in csv_files:
      df = pd.read_csv(file)
      print(file)
      df = df[['SYMBOL','OPEN','HIGH', 'LOW','CLOSE','TIMESTAMP','SERIES']]
      df['STOCK_TUID'] = [uuid.uuid1() for _ in range(len(df.index))]
      df['TIMESTAMP'] = df['TIMESTAMP'].apply(convert_dates)
      df.rename(columns={'SYMBOL': 'STOCK_SYMBOL', 'TIMESTAMP': 'DATE'}, inplace=True)
      df_list.append(df)
  return df_list
