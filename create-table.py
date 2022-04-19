import mysql.connector as msql
import csv
import pandas as pd

db_name = 'dico_db'
file_name = 'dictionnaire'

conn = msql.connect(host='127.0.0.1', user='root',  
                        password='***', db=db_name, charset='utf8')
cursor = conn.cursor()
print('Connected')

df = pd.read_csv(file_name + '.tsv', encoding='utf-8', delimiter='\t')
print('File has been read')

df = df.where(pd.notnull(df), None)
# df = df.drop_duplicates()

# cursor.execute('TRUNCATE dico')

for index, row in df.iterrows():
	id = int(row.iloc[0])
	fr = row.iloc[1] or ''
	ru = row.iloc[2] or ''
	comment = row.iloc[3] or ''
	category = row.iloc[4] or ''
	cursor.execute('INSERT INTO dico VALUES(%s, %s, %s, %s, %s)', 
		(id, fr, ru, comment, category))

conn.commit()
print('Data inserted into table')