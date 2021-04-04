import pandas as pd
import psycopg2
import datetime as dt

from config import *

one_week_ago = (dt.datetime.today() - dt.timedelta(days=4))

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()
cursor.execute('select * from insider_trading')
insider_trading = cursor.fetchall()

if len(insider_trading) > 0:
    latest_in_db = insider_trading[0]

current_it = pd.read_html('http://openinsider.com/insider-purchases-25k')[11]
rm_columns = ['X', '1d', '1w', '1m', '6m']
current_it = current_it[[column for column in current_it.columns if column not in rm_columns]]

for row in current_it.values:
    if len(insider_trading) == 0:
        pass
    
    elif (latest_in_db[0].strftime('%Y-%m-%d') == row[0][:10] and
        latest_in_db[1].strftime('%Y-%m-%d') == row[1] and
        latest_in_db[2] == row[2] and
        latest_in_db[3] == row[3] and
        latest_in_db[4] == row[4] and
        latest_in_db[5] == row[5] and
        float(latest_in_db[6]) == float(row[7][1:]) and
        float(latest_in_db[7]) == float(row[8][1:].replace(',', '')) and
        float(latest_in_db[8]) == float(row[9]) and
        latest_in_db[9] == row[10] and
        float(latest_in_db[10]) == float(row[11][1:].replace(',', '').replace('$', ''))):
        
        break
    
    
    cursor.execute('insert into insider_trading (filing_date, trade_date, ticker, company, insider, title, price, qty, owned, change, value) \
                   values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                   (row[0][:10], row[1], row[2], row[3], row[4], row[5],
                    float(row[7][1:].replace(',', '')),
                    float(row[8].replace(',', '')),
                    row[9], row[10],
                    float(row[11].replace(',', '').replace('$', ''))
                    ))


conn.commit()

cursor.close()
conn.close()