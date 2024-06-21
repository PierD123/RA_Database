import sqlite3 
from pathlib import Path

db_file = Path(__file__).resolve().parent.parent / "retail_app"
#Establish DB connection
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

delete_consumption_table = 'drop table if exists consumption'

cursor.execute(delete_consumption_table)
print("Consumption table has been deleted!")