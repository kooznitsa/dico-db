import mysql.connector as msql
import pandas as pd
import glob


def add_multitran_dict(db_name, file_names, id_num, cat_name, table_name):
    conn = msql.connect(host='127.0.0.1', user='root',  
                            password='akulabutaforia42', db=db_name, charset='utf8')
    cursor = conn.cursor()
    print('Connected')

    # concat and read all *.csv files
    df = pd.concat(map(pd.read_csv, glob.glob(file_names)))
    df.dropna(inplace=True)
    print('File read')

    # set new index starting with the last number in db
    df.insert(0, 'id', range(id_num, id_num + len(df)))

    df['comment'] = ''
    df['category'] = cat_name
    df.rename(columns={'0':'fr', '1':'ru'}, inplace=True)
    df = df.drop('2', axis=1)
    print('DataFrame edited')

    df = df.where(pd.notnull(df), None)

    for index, row in df.iterrows():
        id = int(row.iloc[0])
        fr = row.iloc[1] or ''
        ru = row.iloc[2] or ''
        comment = row.iloc[3] or ''
        category = row.iloc[4] or ''
        cursor.execute('INSERT INTO ' + table_name + ' VALUES(%s, %s, %s, %s, %s)', 
            (id, fr, ru, comment, category))

    conn.commit()
    print('Data inserted into table')


add_multitran_dict(db_name='mt_legal', \
                                file_names='FR/legal/legal*.csv', \
                                id_num=4022, \
                                cat_name='юр.', \
                                table_name='legal_tb')