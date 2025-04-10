import pandas as pd
import sqlite3



db_path = "C:/vicky/Projects/CDT/med_gpt.sqlite3"

connect = sqlite3.connect(db_path)

pd.set_option('display.max_columns', None)

data = pd.read_sql_query("SELECT * FROM dental_analysis" , con=connect)


connect.close()
print(data.tail(1))