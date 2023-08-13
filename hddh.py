from datetime import datetime as dt

year = int(dt.now().strftime("%Y"))
month = int(dt.now().strftime("%m"))
if month < 5:
    year += 1
year = str(year)
print((year))
