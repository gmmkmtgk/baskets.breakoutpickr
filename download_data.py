from process_data import download_bhavcopy_multiple_dates
from datetime import date

#download bhavcopy for the given dates
start_date = date(2021, 8, 28)
end_date = date(2022, 8, 28)
download_bhavcopy_multiple_dates(start_date, end_date)
