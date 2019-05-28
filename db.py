import sqlite3, pandas as pd

conn = sqlite3.connect('test.db')

#describe tables
def describe(table):
    mycur = conn.cursor()
    for row in conn.execute("pragma table_info('" + table + "')").fetchall():
        print(row)

#convert pandas to sqlite
def to_sql(file,db_name):
    df = pd.read_pickle(file)
    df.to_sql(db_name, conn, if_exists='replace', index=False)
    cursor = conn.execute("select * from " + db_name)
    for i in cursor:
        print(i)

#show tables
def show_table():
    mycur = conn.cursor()
    mycur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    available_table=(mycur.fetchall())
    print(available_table)

